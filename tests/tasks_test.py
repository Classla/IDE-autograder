import unittest

from app.tasks import run_input_output_container, run_unit_test_container
from tests.code_examples.sample_request_bodies import (
    input_output_java,
    input_output_python,
    timeout_code,
    unit_test_java,
    unit_test_python,
    unit_test_flawed_python,
    unit_test_flawed_java,
)
from tests.utils.json_to_object import convert_input_output, convert_unit_test


class TestContainerRuntime(unittest.TestCase):
    """Tests the successful execution of each autograder function
    given the direct BaseModel objects of the submissions"""

    # PYTHON
    def test_input_output_python(self):
        result = run_input_output_container(convert_input_output(input_output_python))
        print(result)
        assert result["points"] == 12

    def test_unit_test_python(self):
        """Multiple test files"""
        result = run_unit_test_container(convert_unit_test(unit_test_python))
        assert result["points"] == 12

    def test_unit_test_flawed_python(self):
        """Incomplete points"""
        result = run_unit_test_container(convert_unit_test(unit_test_flawed_python))
        assert result["points"] == 6

        unit_test_flawed_python["autograding_config"][
            "point_calculation"
        ] = "all_or_nothing"
        result = run_unit_test_container(convert_unit_test(unit_test_flawed_python))
        assert result["points"] == 0

    # JAVA
    # def test_input_output_java(self):
    #     result = run_input_output_container(convert_input_output(input_output_java))
    #     assert result["points"] == 12

    # def test_unit_test_java(self):
    #     result = run_unit_test_container(convert_unit_test(unit_test_java))
    #     assert result["points"] == 12

    # def test_unit_test_flawed_java(self):
    #     """Incomplete points"""
    #     result = run_unit_test_container(convert_unit_test(unit_test_flawed_java))
    #     assert result["points"] == 6

    #     unit_test_flawed_java["autograding_config"][
    #         "point_calculation"
    #     ] = "all_or_nothing"
    #     result = run_unit_test_container(convert_unit_test(unit_test_flawed_java))
    #     assert result["points"] == 0

    def test_timeout(self):
        result = run_input_output_container(convert_input_output(timeout_code))
        assert result["msg"] == "Time limit exceeded."


if __name__ == "__main__":
    unittest.main()
