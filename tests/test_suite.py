import unittest
from .main_test import TestUploadEndpoint
from .tasks_test import TestContainerRuntime


def github_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUploadEndpoint))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContainerRuntime))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(github_suite())
