import os
from uuid import UUID

from dotenv import load_dotenv
from supabase import Client, create_client

from app.autograder_container_runtime import create_autograder_container_runtime
from app.autograder_request_bodies import InputOutputRequestBody, UnitTestRequestBody
from app.logging_config import logger
from app.utils import colors

from datetime import datetime

load_dotenv()

supabase: Client = create_client(
    supabase_url=os.environ.get("SUPABASE_URL"),
    supabase_key=os.environ.get("SUPABASE_KEY"),
)

AUTOGRADER_TABLE = "autograder_results"


def send_to_supabase(current_result: dict, block_uuid: UUID, test_uuid: UUID) -> None:
    """handler for updating the supabase table with container output."""
    target_block_uuid = str(block_uuid)
    target_test_uuid = str(test_uuid)
    try:
        target_row: dict = (
            supabase.table(AUTOGRADER_TABLE)
            .select("*")
            .eq("block_uuid", target_block_uuid)
            .eq("autograder_test_uuid", target_test_uuid)
            .execute()
            .data
        )
        if len(target_row) == 0:
            supabase.table(AUTOGRADER_TABLE).insert(
                {
                    "current_result": current_result,
                    "result_history": [],
                    "block_uuid": target_block_uuid,
                    "autograder_test_uuid": target_test_uuid,
                }
            ).execute()

        elif len(target_row) == 1:
            supabase.table(AUTOGRADER_TABLE).update(
                {
                    "current_result": current_result,
                    "result_history": target_row[0]["result_history"]
                    + [target_row[0]["current_result"]],
                }
            ).eq("block_uuid", target_block_uuid).eq(
                "autograder_test_uuid", target_test_uuid
            ).execute()
        else:
            raise Exception(
                "Warning: Table representation is invalid. Multiple rows with matching foreign keys."
            )

    except Exception as e:
        logger.error(f"Failed to insert into table: {str(e)}")
        error_message = f"Error inserting into autograder_results: {str(e)}"
        raise Exception(error_message) from e


def run_input_output_container(submission: InputOutputRequestBody) -> dict:
    """
    Allocates a container, runs the autograding session inside,
    and send the output to supabase.
    """

    expected_stdout: str = submission.input_output_files.expected_stdout.replace(
        '"', '\\"'
    )
    expected_stderr: str = submission.input_output_files.expected_stderr.replace(
        '"', '\\"'
    )
    teacher_stdin: str = submission.input_output_files.teacher_stdin.replace('"', '\\"')

    try:
        # start up container
        container = create_autograder_container_runtime(submission.language)

        # write data to files
        container.write_file(expected_stdout, "expected_stdout.txt")
        container.write_file(expected_stderr, "expected_stderr.txt")
        container.write_file(teacher_stdin, "teacher_stdin.txt")

        container.write_file_tree("", submission.student_files)

        script_execution = container.run_code(
            timeout=submission.timeout,
            entry_file=submission.input_output_config.entry_file,
        )

        if script_execution.exit_code == 124:
            return {
                "autograde_mode": "input_output",
                "msg": "Time limit exceeded.",
                "points": 0,
                "timestamp": datetime.now().isoformat(),
            }

        else:
            stdout_diff_exec_result = container.run_bash(
                f"diff {'-b' if submission.input_output_config.ignore_whitespace else ''} student_stdout.txt expected_stdout.txt"
            )

            stderr_diff_exec_result = container.run_bash(
                f"diff {'-b' if submission.input_output_config.ignore_whitespace else ''} student_stderr.txt expected_stderr.txt"
            )
            stdout_diff = stdout_diff_exec_result.output.decode("utf-8")
            stderr_diff = stderr_diff_exec_result.output.decode("utf-8")

            student_stdout = container.read_file("student_stdout.txt")
            student_stderr = container.read_file("student_stderr.txt")

            logger.info(f"stdout diff: {stdout_diff}")

            return {
                "autograde_mode": "input_output",
                "msg": "Input/Output tests ran successfully.",
                "status_code": 200,
                "stdout_diff": stdout_diff,
                "stderr_diff": stderr_diff,
                "student_stdout": student_stdout,
                "student_stderr": student_stderr,
                "points": (
                    submission.autograding_config.total_points
                    if stdout_diff == stderr_diff == ""
                    else 0
                ),
                "timestamp": datetime.now().isoformat(),
            }

    except Exception as e:
        logger.error(f"Docker container failed: {e}")
        raise Exception() from e

    finally:
        # dispose container
        del container


def run_unit_test_container(submission: UnitTestRequestBody) -> dict:
    """
    Allocates a container, runs the autograding session inside, and send the output to supabase.
    """
    try:
        # start up container
        container = create_autograder_container_runtime(submission.language)

        container.load_unit_test_driver()

        container.write_file_tree("", submission.student_files)

        # Write test files with explicit error handling
        for file_name, file_contents in submission.unit_test_files.items():
            container.write_file(file_contents, f"{file_name}")

        # Run unit tests with explicit error handling
        unit_test_results = container.run_unit_tests(
            timeout=submission.timeout, test_files=submission.unit_test_files
        )

        if unit_test_results.exit_code == 124:
            return {
                "autograde_mode": "unit_test",
                "msg": "Time limit exceeded.",
                "points": 0,
                "timestamp": datetime.now().isoformat(),
            }

        if unit_test_results.exit_code == 1:
            logger.info(unit_test_results.output)
            return {
                "autograde_mode": "unit_test",
                "msg": unit_test_results.output.decode("utf-8"),
                "points": 0,
                "timestamp": datetime.now().isoformat(),
            }

        num_tests = int(container.read_file("num_tests.txt"))
        num_tests_passed = int(container.read_file("num_tests_passed.txt"))
        raise ValueError()
        if submission.autograding_config.point_calculation == "fractional":
            points = (
                num_tests_passed / num_tests
            ) * submission.autograding_config.total_points
        else:  # all or nothing
            points = (
                submission.autograding_config.total_points
                if (num_tests == num_tests_passed)
                else 0
            )

        # logger.error(unit_test_results.output.decode("utf-8"))

        return {
            "autograde_mode": "unit_test",
            "status_code": 200,
            "msg": "Unit tests ran successfully.",
            "unit_test_results": unit_test_results.output.decode("utf-8"),
            "points": points,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Container execution failed: {str(e)}", exc_info=True)
        raise Exception(
            f"Container execution failed with detailed error: {str(e)}"
        ) from e
    finally:
        # Container garbage collection
        if "container" in locals():
            del container
