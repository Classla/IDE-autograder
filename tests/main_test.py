import unittest
from fastapi.testclient import TestClient
from app.main import app
from test_resources.sample_request_bodies import input_output, unit_test


class TestUploadEndpoint(unittest.TestCase):
    """bruh"""

    def setUp(self):
        self.client = TestClient(app)

    def test_input_output_files(self):
        """bruh"""
        response = self.client.post("/input_output/", json=input_output)
        self.assertEqual(response.status_code, 200)
        self.assertIn("output", response.json())

        print(response.json())

    def test_unit_test_files(self):
        """bruh"""
        response = self.client.post("/unit_test/", json=unit_test)

        self.assertEqual(response.status_code, 200)
        self.assertIn("output", response.json())
        print(response.json())


if __name__ == "__main__":
    unittest.main()
