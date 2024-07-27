import os
from abc import ABC, abstractmethod
from typing import Union

import docker
from docker import DockerClient
from docker.models.containers import Container, ExecResult
from dotenv import load_dotenv

from app.logging_config import logger


class AutograderContainerRuntime(ABC):
    def __init__(self, container: Container):
        self._container = container
        self._container.start()

    def _check_success(self, exec_result: ExecResult) -> None:
        exit_code = exec_result.exit_code
        output = exec_result.output
        if exit_code != 0:
            logger.error(f"Command failed with exit code {exit_code}: \n{output}")
            raise RuntimeError()

    def run_bash(self, cmd: str) -> ExecResult:
        """Executes (cmd) in the container and returns the execution result."""
        exec_result = self._container.exec_run(f"bash -c '{cmd}'")
        return exec_result

    def write_file(self, contents: str, path: str) -> None:
        """writes (contents) into the file at (path)"""
        exec_result = self._container.exec_run(f"sh -c 'echo \"{contents}\" > {path}'")
        self._check_success(exec_result)

    def read_file(self, path: str) -> str:
        """returns the contents of the file located at (path)"""
        exec_result = self._container.exec_run(f"bash -c 'cat {path}'")
        self._check_success(exec_result)
        return exec_result.output.decode("utf-8")

    def write_file_tree(self, directory: str, children: Union[str, dict]):
        """Helper function for writing files and directories into the container given a directory."""
        for name, contents in children.items():
            if type(contents) == str:
                self.write_file(contents.replace('"', '\\"'), f"{directory}{name}")
            elif type(contents) == dict:
                self.run_bash(f"mkdir {directory}{name}/")
                self.write_file_tree(f"{directory}{name}/", contents)
            else:
                raise Exception()

    @abstractmethod
    def run_code(self, timeout: int, entry_file: str) -> ExecResult:
        pass

    @abstractmethod
    def load_unit_test_driver(self):
        pass

    @abstractmethod
    def run_unit_tests(self, timeout: int, test_files: dict) -> ExecResult:
        pass

    def __del__(self):
        self._container.stop()
        self._container.remove()


class AutograderContainerRuntimePython(AutograderContainerRuntime):
    def run_code(self, timeout: int, entry_file: str) -> ExecResult:
        return self.run_bash(
            f"timeout {timeout}s python src/{entry_file} < teacher_stdin.txt >student_stdout.txt 2>student_stderr.txt"
        )

    def load_unit_test_driver(self):
        with open(
            "app/container_scripts/unit_test_driver.py", "r", encoding="utf-8"
        ) as file:
            unit_test_driver_data = file.read().replace('"', '\\"')
        self.write_file(unit_test_driver_data, "unit_test_driver.py")

    def run_unit_tests(self, timeout: int, test_files: dict) -> ExecResult:
        return self.run_bash(
            f"timeout {timeout}s python unit_test_driver.py {' '.join([file_name.split('.')[0] for file_name, file_contents in test_files.items()])}"
        )


class AutograderContainerRuntimeJava(AutograderContainerRuntime):

    def run_code(self, timeout: int, entry_file: str) -> ExecResult:

        # build and compile java code
        self._check_success(self.run_bash("javac -d bin src/*.java"))

        # execute
        return self.run_bash(
            f"timeout {timeout}s java -cp bin {entry_file.split('.')[0]} < teacher_stdin.txt >student_stdout.txt 2>student_stderr.txt"
        )

    def load_unit_test_driver(self):
        with open(
            "app/container_scripts/unit_test_driver.py", "r", encoding="utf-8"
        ) as file:
            unit_test_driver_data = file.read().replace('"', '\\"')
        self.write_file(unit_test_driver_data, "unit_test_driver.py")

    def run_unit_tests(self, timeout: int, test_files: dict) -> ExecResult:
        return self.run_bash(
            f"timeout {timeout}s python unit_test_driver.py {' '.join([file_name.split('.')[0] for file_name, file_contents in test_files.items()])}"
        )


load_dotenv()

docker_client: DockerClient = docker.from_env()


def create_autograder_container_runtime(environment: str) -> AutograderContainerRuntime:
    if environment == "python":
        return AutograderContainerRuntimePython(
            docker_client.containers.run(
                "autograder",  # Docker image name
                detach=True,  # run asynchronously
                stdin_open=True,
                mem_limit=os.environ.get(
                    "DOCKER_MEMORY_LIMIT"
                ),  # swap limit default capacity 2x vram limit
            )
        )
    elif environment == "java":
        return AutograderContainerRuntimeJava(
            docker_client.containers.run(
                "autograder_java",  # Docker image name
                detach=True,  # run asynchronously
                stdin_open=True,
                mem_limit=os.environ.get(
                    "DOCKER_MEMORY_LIMIT"
                ),  # swap limit default capacity 2x vram limit
            )
        )
    else:
        raise ValueError(f"Environment '{environment}' is not recognized.")
