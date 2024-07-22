import os
from uuid import UUID

from dotenv import load_dotenv
from supabase import Client, create_client

from app.autograder_requests import InputOutputRequestBody, UnitTestRequestBody
from app.autograder_container_runtime import AutograderContainerRuntime
from app.logging_config import logger
from app.utils import colors


load_dotenv()

supabase: Client = create_client(
    supabase_url=os.environ.get("SUPABASE_URL"),
    supabase_key=os.environ.get("SUPABASE_KEY"),
)

AUTOGRADER_TABLE = "autograder_results"


def send_to_supabase(current_result: dict, block_uuid: UUID) -> None:
    """handler for updating the supabase table with container output."""
    target_block_uuid = str(block_uuid)
    try:
        target_row: dict = (
            supabase.table(AUTOGRADER_TABLE)
            .select("*")
            .eq("block_uuid", target_block_uuid)
            .execute()
            .data
        )
        if len(target_row) == 0:
            supabase.table(AUTOGRADER_TABLE).insert(
                {
                    "current_result": current_result,
                    "result_history": [],
                    "block_uuid": target_block_uuid,
                }
            ).execute()

        elif len(target_row) == 1:
            supabase.table(AUTOGRADER_TABLE).update(
                {
                    "current_result": current_result,
                    "result_history": target_row[0]["result_history"]
                    + [target_row[0]["current_result"]],
                }
            ).eq("block_uuid", target_block_uuid).execute()
        else:
            raise Exception(
                "Warning: Table representation is invalid. Multiple rows with matching foreign keys."
            )

    except Exception as e:
        logger.error(f"Failed to insert into table: {str(e)}")
        error_message = f"Error inserting into autograder_results: {str(e)}"
        raise Exception(error_message) from e


def input_output_autograder(submission: InputOutputRequestBody) -> None:
    """
    Allocates a container, runs the autograding session inside, and send the output to supabase.
    """

    expected_stdout: str = submission.input_output_files.expected_stdout.replace(
        '"', '\\"'
    )
    expected_stderr: str = submission.input_output_files.expected_stderr.replace(
        '"', '\\"'
    )
    teacher_stdin: str = submission.input_output_files.teacher_stdin.replace('"', '\\"')
    entry_file = submission.IDE_settings.entry_file

    try:
        # start up container
        container = AutograderContainerRuntime(
            environment=submission.IDE_settings.language
        )

        # write data to files
        container.write_file(expected_stdout, "expected_stdout.txt")
        container.write_file(expected_stderr, "expected_stderr.txt")
        container.write_file(teacher_stdin, "teacher_stdin.txt")

        for file_name, file_contents in submission.student_files.items():
            container.write_file(
                file_contents.replace('"', '\\"'), f"module/{file_name}"
            )

        script_execution = container.run_bash(
            f"timeout {submission.timeout}s python module/{entry_file} < teacher_stdin.txt >student_stdout.txt 2>student_stderr.txt"
        )

        if script_execution.exit_code == 124:
            send_to_supabase(
                {
                    "autograde_mode": "input_output",
                    "msg": "Time limit exceeded.",
                    "points": 0,
                },
                block_uuid=submission.block_uuid,
            )

        else:
            # run script
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

            logger.info(f"output: {stdout_diff}")

            send_to_supabase(
                {
                    "autograde_mode": "input_output",
                    "msg": "Input/Output tests ran successfully.",
                    "stdout_diff": stdout_diff,
                    "stderr_diff": stderr_diff,
                    "student_stdout": student_stdout,
                    "student_stderr": student_stderr,
                    "points": (
                        submission.autograding_config.total_points
                        if stdout_diff == stderr_diff == ""
                        else 0
                    ),
                },
                block_uuid=submission.block_uuid,
            )

        logger.info("Successfully wrote to table.")

    except Exception as e:
        logger.error(f"Docker container failed: {e}")

    finally:
        # dispose container
        del container


def unit_test_autograder(submission: UnitTestRequestBody) -> None:
    """
    Allocates a container, runs the autograding session inside, and send the output to supabase.
    """

    with open(
        "app/container_scripts/unit_test_driver.py", "r", encoding="utf-8"
    ) as file:
        unit_test_driver_data = file.read().replace('"', '\\"')

    unit_test_driver_path = "unit_test_driver.py"
    try:
        # start up container
        container = AutograderContainerRuntime(
            environment=submission.IDE_settings.language
        )

        # write data to files
        container.write_file(unit_test_driver_data, unit_test_driver_path)

        # Copy student submission files
        for file_name, file_contents in submission.student_files.items():
            file_contents = file_contents.replace('"', '\\"')
            container.write_file(file_contents, f"module/{file_name}")

        # Copy unit test files
        for file_name, file_contents in submission.unit_test_files.items():
            file_contents = file_contents.replace('"', '\\"')
            container.write_file(file_contents, f"tests/{file_name}")

        # run unit tests
        unit_test_results = container.run_bash(
            f"timeout {submission.timeout}s python {unit_test_driver_path} {' '.join([file_name.split('.')[0] for file_name, file_contents in submission.unit_test_files.items()])}"
        )

        if unit_test_results.exit_code == 124:
            send_to_supabase(
                {
                    "autograde_mode": "unit_test",
                    "msg": "Time limit exceeded.",
                    "points": 0,
                },
                block_uuid=submission.block_uuid,
            )

        else:
            num_tests = int(container.read_file("num_tests.txt"))
            num_tests_passed = int(container.read_file("num_tests_passed.txt"))

            if submission.autograding_config.point_calculation == "fractional":
                points = (
                    num_tests_passed / num_tests
                ) * submission.autograding_config.total_points
            else:
                points = (
                    submission.autograding_config.total_points
                    if (num_tests == num_tests_passed)
                    else 0
                )

            logger.info(
                f"Unit test output: {colors.YELLOW}{unit_test_results.output.decode('utf-8')}{colors.RESET}"
            )
            send_to_supabase(
                {
                    "autograde_mode": "unit_test",
                    "unit_test_results": unit_test_results.output.decode("utf-8"),
                    "points": points,
                },
                block_uuid=submission.block_uuid,
            )

        logger.info("Successfully wrote to table.")
    except Exception as e:
        logger.error(
            f"An error occured during the execution of a docker container: {e}"
        )
    finally:
        # container no longer in use
        del container
