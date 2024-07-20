import os
from uuid import UUID

import docker
from docker import DockerClient
from docker.models.containers import Container
from dotenv import load_dotenv
from supabase import Client, create_client

from app.autograder_classes import InputOutputRequestBody, UnitTestRequestBody
from app.logging_config import logger
from app.utils import colors

load_dotenv()

docker_client: DockerClient = docker.from_env()

supabase: Client = create_client(
    supabase_url=os.environ.get("SUPABASE_URL"),
    supabase_key=os.environ.get("SUPABASE_KEY"),
)

AUTOGRADER_TABLE = "autograder_results"


def run_autograder_container() -> Container:
    """Run a container image with custom settings"""
    return docker_client.containers.run(
        "autograder",  # Docker image name
        detach=True,  # run asynchronously
        stdin_open=True,
        mem_limit=os.environ.get(
            "DOCKER_MEMORY_LIMIT"
        ),  # swap limit default capacity 2x vram limit
    )


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

    try:
        # start up container
        container = run_autograder_container()
        container.start()

        # write data to files
        container.exec_run(f"sh -c 'echo \"{expected_stdout}\" > expected_stdout.txt'")
        container.exec_run(f"sh -c 'echo \"{expected_stderr}\" > expected_stderr.txt'")
        container.exec_run(f"sh -c 'echo \"{teacher_stdin}\" > teacher_stdin.txt'")

        for file_name, file_contents in submission.student_files.items():
            file_contents = file_contents.replace('"', '\\"')
            container.exec_run(f"sh -c 'echo \"{file_contents}\" > module/{file_name}'")

        script_execution = container.exec_run(
            f"bash -c 'timeout {submission.timeout}s python module/{submission.IDE_settings.entry_file} < teacher_stdin.txt >student_stdout.txt 2>student_stderr.txt'"
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

        # run script
        stdout_diff_exec_result = container.exec_run(
            f"bash -c 'diff {'-b' if submission.input_output_config.ignore_whitespace else ''} student_stdout.txt expected_stdout.txt'"
        )

        stderr_diff_exec_result = container.exec_run(
            f"bash -c 'diff {'-b' if submission.input_output_config.ignore_whitespace else ''} student_stderr.txt expected_stderr.txt'"
        )

        student_stdout = container.exec_run(
            "bash -c 'cat student_stdout.txt'"
        ).output.decode("utf-8")
        student_stderr = container.exec_run(
            "bash -c 'cat student_stderr.txt'"
        ).output.decode("utf-8")
        stdout_diff = stdout_diff_exec_result.output.decode("utf-8")
        stderr_diff = stderr_diff_exec_result.output.decode("utf-8")

        logger.info(f"output: {stdout_diff}")

    except Exception as e:
        logger.error(f"Docker container failed: {e}")
        raise Exception(
            f"An error occured during the execution of a docker container: {e}"
        ) from e

    finally:
        # container no longer in use
        container.stop()
        container.remove()

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


def unit_test_autograder(submission: UnitTestRequestBody) -> None:
    """
    Allocates a container, runs the autograding session inside, and send the output to supabase.
    """

    submission_data = submission.files_data[0].content.replace('"', '\\"')
    test_data = submission.files_data[1].content.replace('"', '\\"')

    with open(
        "app/container_scripts/unit_test_driver.py", "r", encoding="utf-8"
    ) as file:
        unit_test_driver_data = file.read().replace('"', '\\"')
    submission_path = "/app/submission.py"
    test_path = "/app/unit_tests.py"
    unit_test_driver_path = "/app/unit_test_driver.py"

    try:
        # start up container
        container = run_autograder_container()
        container.start()

        # write data to files
        container.exec_run(f"sh -c 'echo \"{submission_data}\" > {submission_path}'")
        container.exec_run(f"sh -c 'echo \"{test_data}\" > {test_path}'")
        container.exec_run(
            f"sh -c 'echo \"{unit_test_driver_data}\" > {unit_test_driver_path}'"
        )
        container.exec_run("sh -c 'echo \"print()\" > app/__init__.py'")

        # run script
        exec_result = container.exec_run(
            f"bash -c 'python {unit_test_driver_path}'"
        ).output.decode("utf-8")

        logger.info(f"Unit test output: {colors.YELLOW}{exec_result}")
    except Exception as e:
        logger.error(
            f"An error occured during the execution of a docker container: {e}"
        )
        raise Exception(
            f"An error occured during the execution of a docker container: {e}"
        ) from e
    finally:
        # container no longer in use
        container.stop()
        container.remove()

    send_to_supabase(
        {
            "autograde_mode": "unit_test",
            "stdout": exec_result.output.decode("utf-8"),
        },
        block_uuid=submission.block_uuid,
    )

    logger.info("Successfully wrote to table.")
