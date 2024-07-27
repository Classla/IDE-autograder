import unittest

from fastapi.testclient import TestClient
from utils.json_to_object import convert_input_output, convert_unit_test

from app.main import app, autograder_job
from test_resources.sample_request_bodies import input_output_python, unit_test_python


class TestUploadEndpoint(unittest.TestCase):
    """Test a http call to the api endpoint"""

    def setUp(self):
        self.client = TestClient(app)

    def test_input_output_endpoint(self):
        """bruh"""
        response = self.client.post("/input_output/", json=input_output_python)
        self.assertEqual(response.status_code, 200)
        self.assertIn("output", response.json())

        print(response.json())

    def test_unit_test_endpoint(self):
        """bruh"""
        response = self.client.post("/unit_test/", json=unit_test_python)

        self.assertEqual(response.status_code, 200)
        self.assertIn("output", response.json())
        print(response.json())


class TestAutograderJob(unittest.TestCase):
    """_summary_"""

    def test_autograder_job_input_output_python(self):
        autograder_job(convert_input_output(input_output_python))

    def test_autograder_job_unit_test_python(self):
        autograder_job(convert_unit_test(unit_test_python))


if __name__ == "__main__":
    unittest.main()
