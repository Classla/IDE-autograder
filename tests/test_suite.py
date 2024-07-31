import unittest
from .main_test import TestUploadEndpoint


def github_suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUploadEndpoint))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(github_suite())
