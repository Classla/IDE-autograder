input_output = {
    "block_uuid": "7ceb06fa-5d44-4fc2-8aa9-2aaa8b743e65",
    "timeout": 10,
    "student_files": {
        "main.py": 'from mod import apple; print(f"hello, {input()}! number: {apple}")',
        "mod.py": "apple = 42",
    },
    "IDE_settings": {"language": "python", "entry_file": "main.py"},
    "autograding_config": {
        "total_points": 12,
        "point_calculation": "all_or_nothing",
    },
    "input_output_config": {"ignore_whitespace": False},
    "input_output_files": {
        "expected_stdout": "hello, apples!",
        "expected_stderr": "",
        "teacher_stdin": "apples",
    },
}


with open("test_resources/add.py", "r", encoding="utf-8") as file:
    script = file.read()
with open("test_resources/test_add.py", "r", encoding="utf-8") as file:
    test = file.read()

unit_test = {
    "files_data": [
        {
            "id": "1",
            "name": "submission.py",
            "type": "python",
            "content": script,
        },
        {"id": "2", "name": "unittest.py", "type": "text", "content": test},
    ],
    "IDE_settings_data": {
        "language": "python",
        "default_run_file": {"id": "1", "name": "submission.py"},
    },
    "test_case_data": {
        "type": "unit",
        "title": "Sample Test",
        "points": 10,
        "input": "Hello",
        "expected_output": "Hello, world!",
    },
}
