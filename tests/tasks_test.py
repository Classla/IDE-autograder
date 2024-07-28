import unittest

from utils.json_to_object import convert_input_output, convert_unit_test

from test_resources.sample_request_bodies import (
    input_output_java,
    input_output_python,
    unit_test_java,
    unit_test_python,
)

from app.tasks import run_input_output_container, run_unit_test_container


class TestContainerRuntime(unittest.TestCase):
    """Tests the successful execution of each autograder function
    given the direct BaseModel objects of the submissions"""

    def test_input_output_python(self):
        result = run_input_output_container(convert_input_output(input_output_python))
        print(result)
        assert result["points"] == 12

    def test_unit_test_python(self):
        result = run_unit_test_container(convert_unit_test(unit_test_python))
        assert result["points"] == 12

    def test_input_output_java(self):
        result = run_input_output_container(convert_input_output(input_output_java))
        assert result["points"] == 12

    def test_unit_test_java(self):
        result = run_unit_test_container(convert_unit_test(unit_test_java))
        assert result["points"] == 12


if __name__ == "__main__":
    unittest.main()
