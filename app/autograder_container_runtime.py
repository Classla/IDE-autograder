import os

import docker
from docker import DockerClient
from docker.models.containers import Container, ExecResult
from dotenv import load_dotenv
from app.logging_config import logger

load_dotenv()

docker_client: DockerClient = docker.from_env()


class AutograderContainerRuntime:
    def __init__(self):
        self._container: Container = docker_client.containers.run(
            "autograder",  # Docker image name
            detach=True,  # run asynchronously
            stdin_open=True,
            mem_limit=os.environ.get(
                "DOCKER_MEMORY_LIMIT"
            ),  # swap limit default capacity 2x vram limit
        )
        self._container.start()

    def run_bash(self, cmd: str) -> ExecResult:
        exec_result = self._container.exec_run(f"bash -c '{cmd}'")
        return exec_result

    def _check_success(self, exec_result: ExecResult) -> None:
        if exec_result.exit_code != 0:
            logger.error("Command failed. To debug, fill in this error message.")

    def write_file(self, contents: str, path: str) -> None:
        exec_result = self._container.exec_run(f"sh -c 'echo \"{contents}\" > {path}'")
        self._check_success(exec_result)

    def read_file(self, path: str) -> str:
        exec_result = self._container.exec_run(f"bash -c 'cat {path}'")
        self._check_success(exec_result)
        return exec_result.output.decode("utf-8")

    def __del__(self):
        self._container.stop()
        self._container.remove()
