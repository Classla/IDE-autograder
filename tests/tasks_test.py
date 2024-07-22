import json
import unittest

from pydantic import TypeAdapter

from app.autograder_requests import InputOutputRequestBody, UnitTestRequestBody
from app.tasks import input_output_autograder, unit_test_autograder
from test_resources.sample_request_bodies import input_output, unit_test


class TestAutograderJobs(unittest.TestCase):
    """Tests the successful execution of each autograder function
    given the direct BaseModel objects of the submissions"""

    def test_input_output_files(self):
        submission: InputOutputRequestBody = TypeAdapter(
            InputOutputRequestBody
        ).validate_json(json.dumps(input_output))

        input_output_autograder(submission)

    def test_unit_test_files(self):
        submission: UnitTestRequestBody = TypeAdapter(
            UnitTestRequestBody
        ).validate_json(json.dumps(unit_test))

        unit_test_autograder(submission)


if __name__ == "__main__":
    unittest.main()
