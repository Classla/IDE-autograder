import os
from typing import Dict, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


def check_file_extensions(cls, value):
    """Verify certain fields are valid files"""
    for filename in value.keys():
        if not os.path.splitext(filename)[1]:  # Check if there's a file extension
            raise ValueError(f"File '{filename}' does not have a valid file extension.")
    return value


class AutograderRequestBody(BaseModel):
    class IDESettings(BaseModel):
        language: Literal["python", "java"] = Field(
            ..., description="Programming language"
        )
        entry_file: str = Field(
            ..., description="Entry file for the autograder"
        )  # this may not be needed for a unit test

    class AutogradingConfig(BaseModel):
        total_points: int = Field(..., ge=0, description="Total points for grading")
        point_calculation: Literal["all_or_nothing", "fractional"] = Field(
            ...,
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

    _check_student_files = validator("student_files", allow_reuse=True)(
        check_file_extensions
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

    unit_test_config: Optional[Dict]  # empty for now
    unit_test_files: Dict[str, str] = Field(
        ..., description="Dictionary of unit test files"
    )

    _check_unit_test_files = validator("unit_test_files", allow_reuse=True)(
        check_file_extensions
    )
