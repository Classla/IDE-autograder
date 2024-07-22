import unittest
import sys

# List of test filenames (without the .py extension)
test_files = sys.argv[1:]

# Create a test suite
suite = unittest.TestSuite()

# Load tests from each test file
loader = unittest.TestLoader()
for test_file in test_files:
    suite.addTests(loader.loadTestsFromName(f"{test_file}"))

# Run the test suite
runner = unittest.TextTestRunner()
result = runner.run(suite)

# Calculate the number of tests passed
num_tests = result.testsRun
num_tests_passed = num_tests - len(result.failures) - len(result.errors)

with open("num_tests.txt", "w") as file:
    file.write(str(num_tests))

with open("num_tests_passed.txt", "w") as file:
    file.write(str(num_tests_passed))
