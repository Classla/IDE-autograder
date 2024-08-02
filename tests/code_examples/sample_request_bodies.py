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

timeout_code = {
    "block_uuid": block_uuid,
    "timeout": 1,
    "student_files": {
        "main.py": "import time; time.sleep(2)",
    },
    "IDE_settings": {"language": "python", "entry_file": "main.py"},
    "autograding_config": {
        "total_points": 12,
        "point_calculation": "all_or_nothing",
    },
    "input_output_config": {"ignore_whitespace": False},
    "input_output_files": {
        "expected_stdout": "",
        "expected_stderr": "",
        "teacher_stdin": "",
    },
}


with open("tests/code_examples/add.py", "r", encoding="utf-8") as file:
    script_python = file.read()
with open("tests/code_examples/test_add.py", "r", encoding="utf-8") as file:
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
        "Main.java": 'import modules.Module;import java.util.Scanner;public class Main {public static void main(String[] args) {Scanner scanner = new Scanner(System.in);System.out.print("");String name = scanner.nextLine();System.out.printf("hello, %s! number: %d %d%n", name, Mod.APPLE, Module.ORANGE);scanner.close();}}',
        "Mod.java": "public class Mod {public static final int APPLE = 42;}",
        "modules": {
            "Module.java": "package modules;public class Module {public static final int ORANGE = 69;}"
        },
    },
    "IDE_settings": {"language": "java", "entry_file": "Main.java"},
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
with open("tests/code_examples/Add.java", "r", encoding="utf-8") as file:
    script_java = file.read()
with open("tests/code_examples/TestAdd.java", "r", encoding="utf-8") as file:
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
