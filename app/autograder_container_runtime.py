import os
import base64
from abc import ABC, abstractmethod
from typing import Union

import docker
from docker import DockerClient
from docker.models.containers import Container, ExecResult
from dotenv import load_dotenv

from app.logging_config import logger


DOCKER_MEMORY_LIMIT = (
    os.environ.get("DOCKER_MEMORY_LIMIT")
    if os.environ.get("DOCKER_MEMORY_LIMIT")
    else "500m"
)


class AutograderContainerRuntime(ABC):
    def __init__(self, container: Container):
        self._container = container
        self._container.start()

    def _check_success(self, exec_result: ExecResult) -> None:
        exit_code = exec_result.exit_code
        output = exec_result.output
        if exit_code != 0:
            logger.error(
                f"Docker shell command failed with exit code {exit_code}: \n{output}"
            )
            raise RuntimeError()

    def run_bash(self, cmd: str) -> ExecResult:
        """Executes (cmd) in the container and returns the execution result."""
        exec_result = self._container.exec_run(f"bash -c '{cmd}'")
        return exec_result

    def write_file(self, contents: str, path: str) -> None:
        """
        Writes (contents) into the file at (path) using base64 encoding to handle special characters.
        """
        # Encode the contents as base64
        encoded_contents = base64.b64encode(contents.encode("utf-8")).decode("utf-8")

        # Use base64 decode in the container to write the file
        exec_result = self._container.exec_run(
            f"sh -c 'echo {encoded_contents} | base64 -d > {path}'"
        )
        self._check_success(exec_result)

    def read_file(self, path: str) -> str:
        """Returns the contents of the file located at (path)"""
        exec_result = self._container.exec_run(f"bash -c 'cat {path}'")
        self._check_success(exec_result)
        return exec_result.output.decode("utf-8")

    def write_file_tree(self, directory: str, children: Union[str, dict]):
        """Helper function for writing files and directories into the container given a directory."""
        for name, contents in children.items():
            if isinstance(contents, str):
                self.write_file(contents, f"{directory}{name}")
            elif isinstance(contents, dict):
                self.run_bash(f"mkdir -p {directory}{name}/")
                self.write_file_tree(f"{directory}{name}/", contents)
            else:
                raise Exception(f"Unexpected type for contents: {type(contents)}")

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
            f"xvfb-run -a timeout {timeout}s python src/{entry_file} < teacher_stdin.txt >student_stdout.txt 2>student_stderr.txt"
        )

    def load_unit_test_driver(self):
        with open(
            "app/unit_test_drivers/unit_test_driver.py", "r", encoding="utf-8"
        ) as file:
            self.write_file(file.read(), "unit_test_driver.py")

    def run_unit_tests(self, timeout: int, test_files: dict) -> ExecResult:
        exec_result = self.run_bash(
            f"xvfb-run -a timeout {timeout}s python unit_test_driver.py {' '.join([file_name.split('.')[0] for file_name, file_contents in test_files.items()])}"
        )
        self._check_success(exec_result)

        # raise Exception(self.run_bash("ls").output.decode("utf-8"))

        return exec_result


class AutograderContainerRuntimeJava(AutograderContainerRuntime):
    def run_code(self, timeout: int, entry_file: str) -> ExecResult:
        # build and compile java code
        self._check_success(self.run_bash('javac -d bin $(find src -name "*.java")'))

        # execute
        return self.run_bash(
            f"timeout {timeout}s java -cp bin {entry_file.split('.')[0]} < teacher_stdin.txt >student_stdout.txt 2>student_stderr.txt"
        )

    def load_unit_test_driver(self):
        with open(
            "app/unit_test_drivers/UnitTestDriver.java", "r", encoding="utf-8"
        ) as file:
            self.write_file(file.read(), "UnitTestDriver.java")

    def run_unit_tests(self, timeout: int, test_files: dict) -> ExecResult:
        # build and compile java code
        self._check_success(
            self.run_bash(
                'javac -cp .:junit-platform-console-standalone.jar -d bin $(find src -name "*.java") tests/*.java UnitTestDriver.java'
            )
        )

        # Run tests
        return self.run_bash(
            f"timeout {timeout}s java -cp bin:junit-platform-console-standalone.jar UnitTestDriver {' '.join([file_name.split('.')[0] for file_name, _ in test_files.items()])}"
        )


load_dotenv()

docker_client: DockerClient = docker.from_env()


def create_autograder_container_runtime(environment: str) -> AutograderContainerRuntime:
    if environment == "python":
        return AutograderContainerRuntimePython(
            docker_client.containers.run(
                "dockerfile_python",  # Docker image name
                detach=True,  # run asynchronously
                stdin_open=True,
                mem_limit=DOCKER_MEMORY_LIMIT,  # swap limit default capacity 2x vram limit
            )
        )
    elif environment == "java":
        return AutograderContainerRuntimeJava(
            docker_client.containers.run(
                "dockerfile_java",  # Docker image name
                detach=True,  # run asynchronously
                stdin_open=True,
                mem_limit=DOCKER_MEMORY_LIMIT,  # swap limit default capacity 2x vram limit
            )
        )
    else:
        raise ValueError(f"Environment '{environment}' is not recognized.")
