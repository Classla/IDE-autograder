block_uuid = "7ceb06fa-5d44-4fc2-8aa9-2aaa8b743e65"
timeout = 10

input_output_python = {
    "block_uuid": block_uuid,
    "timeout": timeout,
    "student_files": {
        "main.py": 'from mod import apple; from modules.module import orange; print(f"hello, {input()}! number: {apple} {orange}")',
        "mod.py": "apple = 42",
        "modules": {"module.py": "orange = 69"},
    },
    "IDE_settings": {"language": "python", "entry_file": "main.py"},
    "autograding_config": {
        "total_points": 12,
        "point_calculation": "all_or_nothing",
    },
    "input_output_config": {"ignore_whitespace": False},
    "input_output_files": {
        "expected_stdout": "hello, apples! number: 42 69\n",
        "expected_stderr": "",
        "teacher_stdin": "apples",
    },
}


with open("test_resources/add.py", "r", encoding="utf-8") as file:
    script_python = file.read()
with open("test_resources/test_add.py", "r", encoding="utf-8") as file:
    test_python = file.read()

unit_test_python = {
    "block_uuid": block_uuid,
    "timeout": timeout,
    "student_files": {"add.py": script_python},
    "IDE_settings": {"language": "python", "entry_file": "main.py"},
    "autograding_config": {
        "total_points": 12,
        "point_calculation": "fractional",
    },
    "unit_test_config": {},
    "unit_test_files": {
        "test_add.py": test_python,
    },
}


input_output_java = {
    "block_uuid": block_uuid,
    "timeout": timeout,
    "student_files": {
        "Main.java": 'public class Main {public static void main(String[] args) {System.out.println("Hello, World!");}}',
    },
    "IDE_settings": {"language": "java", "entry_file": "Main.java"},
    "autograding_config": {
        "total_points": 12,
        "point_calculation": "all_or_nothing",
    },
    "input_output_config": {"ignore_whitespace": False},
    "input_output_files": {
        "expected_stdout": "Hello, World!\n",
        "expected_stderr": "",
        "teacher_stdin": "",
    },
}

with open("test_resources/Add.java", "r", encoding="utf-8") as file:
    script_java = file.read()
with open("test_resources/TestAdd.java", "r", encoding="utf-8") as file:
    test_java = file.read()

unit_test_java = {
    "block_uuid": block_uuid,
    "timeout": timeout,
    "student_files": {"Add.java": script_java},
    "IDE_settings": {"language": "java", "entry_file": "bruh"},
    "autograding_config": {
        "total_points": 12,
        "point_calculation": "fractional",
    },
    "unit_test_config": {},
    "unit_test_files": {
        "TestAdd.java": test_java,
    },
}
