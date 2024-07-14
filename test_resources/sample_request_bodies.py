input_output = {
    "files_data": [
        {
            "id": "1",
            "name": "submission.py",
            "type": "python",
            "content": "print('Hello, world!')",
        },
        {"id": "2", "name": "input.txt", "type": "text", "content": "Hello"},
        {
            "id": "3",
            "name": "expected_output.txt",
            "type": "text",
            "content": "Hello, world!",
        },
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
