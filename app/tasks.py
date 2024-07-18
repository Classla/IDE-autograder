import os

import docker
from docker.models.containers import Container
from docker import DockerClient
from dotenv import load_dotenv
from supabase import Client, create_client

from app.logging_config import logger
from app.autograder_classes import InputOutputRequestBody, UnitTestRequestBody
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


def send_to_supabase(current_result: dict) -> None:
    """handler for updating the supabase table with container output."""
    target_block_uuid: str = current_result["block_uuid"]
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

    expected_stdout_path = "expected_stdout.txt"
    expected_stderr_path = "expected_stderr.txt"
    teacher_stdin_path = "teacher_stdin.txt"

    try:
        # start up container
        container = run_autograder_container()
        container.start()

        # write data to files
        container.exec_run(
            f"sh -c 'echo \"{expected_stdout}\" > {expected_stdout_path}'"
        )
        container.exec_run(
            f"sh -c 'echo \"{expected_stderr}\" > {expected_stderr_path}'"
        )
        container.exec_run(f"sh -c 'echo \"{teacher_stdin}\" > {teacher_stdin_path}'")

        for file_name, file_contents in submission.student_files.items():
            file_contents = file_contents.replace('"', '\\"')
            container.exec_run(f"sh -c 'echo \"{file_contents}\" > module/{file_name}'")

        # run script
        exec_result = container.exec_run(
            f"bash -c 'diff {'-b' if submission.input_output_config.ignore_whitespace else ''} <(python module/{submission.IDE_settings.entry_file} < {teacher_stdin_path}) {expected_stdout_path}'"
        )

        logger.info(exec_result.output.decode("utf-8"))

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
            "stdout": exec_result.output.decode("utf-8"),
            "block_uuid": submission.block_uuid,
        }
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
        }
    )

    logger.info("Successfully wrote to table.")
