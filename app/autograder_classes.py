from pydantic import BaseModel
from typing import List


class FileData(BaseModel):
    id: str
    name: str
    type: str
    content: str


class IDESettingsData(BaseModel):
    class DefaultRunFile(BaseModel):
        id: str
        name: str

    language: str
    default_run_file: DefaultRunFile


class TestCaseData(BaseModel):
    type: str
    title: str
    points: int
    input: str
    expected_output: str


class ProjectData(BaseModel):
    files_data: List[FileData]
    IDE_settings_data: IDESettingsData
    test_case_data: TestCaseData
