# App

## Folder Structure

```
app/
├── container_scripts/
│   ├── unit_test_driver.py
│   └── ...
├── utils/
│   ├── colors.py           # Custom module for colored logging
│   └── ...
├── autograder_container_runtime.py   # Runtime classes for each container environment
├── autograder_requests.py  # Classes to validate request bodies
├── logging_config.py       # Logging configuration
├── main.py                 # Main FastAPI application entry point
├── tasks.py                # Background tasks
└── ...
```

## Request Body Format

```json
{
  "block_uuid": "block_uuid",
  "test_uuid": "test_uuid",
  "timeout": "int in seconds",
  "student_files": {
    "filename": "file contents"
  },
  "language": "python",
  "autograding_config": {
    "total_points": 12,
    "point_calculation": "all_or_nothing or fractional"
  },
  "unit_test_config": {},
  "input_output_config": { "ignore_whitespace": true, "entry_file": "main.py" },
  "unit_test_files": {
    "filename": "file contents"
  },
  "input_output_files": {
    "expected_stdout": "",
    "expected_stderr": "",
    "teacher_stdin": ""
  }
}
```

## Container Runtime File Structure - Input/Output

```
app/
├── expected_stdout.txt
├── expected_stderr.txt
├── teacher_stdin.txt
├── src/
|   ├── entry_file          # Entry file
│   └── ...                 # Student files
└── tests/                  # Empty tests directory
```

## Container Runtime File Structure - Unit Test

```
app/
├── unit_test_driver.py
├── num_tests.txt           # Unit test driver write the total tests to this file
├── num_tests_passed.txt    # Unit test driver write the # of tests passed to this file
├── src/
│   └── ...                 # Student files
├── tests/                  # Empty tests directory
|   └── ...                 # Test files
└── ...
```
