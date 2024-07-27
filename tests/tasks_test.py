import json
import unittest

from pydantic import TypeAdapter

from app.autograder_requests import InputOutputRequestBody, UnitTestRequestBody
from app.tasks import run_input_output_container, unit_test_autograder
from test_resources.sample_request_bodies import (
    input_output_python,
    unit_test_python,
    input_output_java,
    unit_test_java,
)


class TestAutograderJobs(unittest.TestCase):
    """Tests the successful execution of each autograder function
    given the direct BaseModel objects of the submissions"""

    @staticmethod
    def _test_input_output(file):
        submission: InputOutputRequestBody = TypeAdapter(
            InputOutputRequestBody
        ).validate_json(json.dumps(file))

        result = run_input_output_container(submission)
        assert type(result) == dict

    @staticmethod
    def _test_unit_test(file):
        submission: UnitTestRequestBody = TypeAdapter(
            UnitTestRequestBody
        ).validate_json(json.dumps(file))

        unit_test_autograder(submission)

    def test_input_output_python(self):
        self._test_input_output(input_output_python)

    def test_unit_test_python(self):
        self._test_unit_test(unit_test_python)

    def test_input_output_java(self):
        self._test_input_output(input_output_java)

    def test_unit_test_java(self):
        self._test_unit_test(unit_test_java)


if __name__ == "__main__":
    unittest.main()
