import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.autograder_classes import ProjectData
from test_resources.sample_request_bodies import input_output, unit_test


# We mock this function so that supabase doesn't get written as a side effect
def mock_run_docker_job(project_data: ProjectData, mode: str) -> None:
    """
    Allocates a container, runs the autograding session inside, and send the output to supabase.
    """
    assert isinstance(project_data, ProjectData)
    assert isinstance(mode, str)

    if mode == "input_output":
        pass
    elif mode == "unit_test":
        pass
    else:
        raise ValueError(f"Unrecognized mode: {mode}")

    # start up container
    # write data to files
    # run script
    # container no longer in use
    # send to supabase


class TestUploadEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.tasks.run_docker_job", new=mock_run_docker_job)
    def test_input_output_files(self):

        response = self.client.post("/input_output/", json=input_output)
        self.assertEqual(response.status_code, 200)
        self.assertIn("output", response.json())

        print(response.json())

    @patch("app.tasks.run_docker_job", new=mock_run_docker_job)
    def test_unit_test_files(self):
        response = self.client.post("/unit_test/", json=unit_test)

        self.assertEqual(response.status_code, 200)
        self.assertIn("output", response.json())
        print(response.json())


if __name__ == "__main__":
    unittest.main()
