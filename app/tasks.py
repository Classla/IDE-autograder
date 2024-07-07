import os
import logging

from app.autograder_classes import ProjectData

import docker
from docker import DockerClient
from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

docker_client: DockerClient = docker.from_env()

supabase: Client = create_client(
    supabase_url=os.environ.get("SUPABASE_URL"),
    supabase_key=os.environ.get("SUPABASE_KEY"),
)


def run_docker_job(project_data: ProjectData, mode: str) -> str:
    """
    Allocates a container, runs the autograding session inside, and send the output to supabase.
    """
    if mode == "input_output":
        submission_data = project_data.files_data[0].content.replace('"', '\\"')
        sample_input_data = project_data.files_data[1].content.replace('"', '\\"')
        expected_output_data = project_data.files_data[2].content.replace('"', '\\"')

        submission_path = "/app/submission.py"
        sample_input_path = "/app/input.txt"
        expected_output_path = "/app/expected_output.txt"

    elif mode == "unit_test":
        submission_data = project_data.files_data[0].content.replace('"', '\\"')
        test_data = project_data.files_data[1].content.replace('"', '\\"')

        submission_path = "/app/submission.py"
        test_path = "/app/test.py"
    else:
        raise ValueError(f"Unrecognized mode: {mode}")

    # start up container
    container = docker_client.containers.run(
        "autograder",  # Docker image name
        detach=True,  # run asynchronously
        stdin_open=True,
    )
    container.start()

    if mode == "input_output":
        # write data to files
        container.exec_run(f"sh -c 'echo \"{submission_data}\" > {submission_path}'")
        container.exec_run(
            f"sh -c 'echo \"{sample_input_data}\" > {sample_input_path}'"
        )
        container.exec_run(
            f"sh -c 'echo \"{expected_output_data}\" > {expected_output_path}'"
        )

        # run script
        exec_result = container.exec_run(
            f"bash -c 'diff <(python {submission_path} < {sample_input_path}) {expected_output_path}'"
        )
    elif mode == "unit_test":
        # write data to files
        container.exec_run(f"sh -c 'echo \"{submission_data}\" > {submission_path}'")
        container.exec_run(f"sh -c 'echo \"{test_data}\" > {test_path}'")

        # run script
        exec_result = container.exec_run(f"bash -c 'python {test_path}'")

    logging.info(exec_result.output.decode("utf-8"))

    # container no longer in use
    container.stop()
    container.remove()

    output = exec_result.output.decode("utf-8")

    try:
        supabase.table("autograder_results").insert(
            {
                "current_result": {"output": output},
                "result_history": [{"example_key": "example_value"}],  # TODO: Fill in
            }
        ).execute()

    except Exception as e:
        error_message = f"Error inserting into autograder_results: {str(e)}"
        raise Exception(error_message)
