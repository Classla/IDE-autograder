from typing import Dict, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AutograderRequestBody(BaseModel):
    class IDESettings(BaseModel):
        language: str = Field(..., description="Programming language")
        entry_file: str = Field(..., description="Entry file for the autograder")

    class AutogradingConfig(BaseModel):
        total_points: int = Field(..., description="Total points for grading")
        point_calculation: Literal["all_or_nothing", "fractional"] = Field(
            ...,
            ge=0,
            description="Point calculation method, either 'all_or_nothing' or 'fractional'",
        )

    block_uuid: UUID = Field(
        ..., description="UUID for the block that the code lives on."
    )
    timeout: int = Field(..., ge=1, le=30, description="Timeout in seconds")
    student_files: Dict[str, str] = Field(
        ...,
        description="Dictionary of student code files such that the the filename maps to the file contents",
    )
    IDE_settings: IDESettings = Field(..., description="IDE settings")
    autograding_config: AutogradingConfig = Field(
        ..., description="Autograding configuration"
    )


class InputOutputRequestBody(AutograderRequestBody):
    class InputOutputFiles(BaseModel):
        expected_stdout: str = Field(..., description="Expected standard output")
        expected_stderr: str = Field(..., description="Expected standard error")
        teacher_stdin: str = Field(..., description="Teacher-provided standard input")

    class InputOutputConfig(BaseModel):
        ignore_whitespace: bool = Field(
            ..., description="Ignore whitespace in unit tests"
        )

    input_output_files: InputOutputFiles = Field(..., description="Input-output files")
    input_output_config: InputOutputConfig = Field(
        ..., description="Unit test configuration"
    )


class UnitTestRequestBody(AutograderRequestBody):
    class UnitTestFiles(BaseModel):
        filename: str = Field(..., description="Contents of the unit test file")

    unit_test_config: Optional[Dict]  # empty for now
    unit_test_files: Dict[str, UnitTestFiles] = Field(
        ..., description="Dictionary of unit test files"
    )
