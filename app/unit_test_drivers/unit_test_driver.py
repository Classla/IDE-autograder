import unittest
import sys

# List of test filenames (without the .py extension)
test_files = sys.argv[1:]

# Create a test suite
suite = unittest.TestSuite()

# Load tests from each test file
loader = unittest.TestLoader()

num_tests = 0
num_tests_passed = 0

with open("num_tests.txt", "w") as file:
    file.write(str(num_tests))

with open("num_tests_passed.txt", "w") as file:
    file.write(str(num_tests_passed))


try:
    for test_file in test_files:
        try:
            tests = loader.loadTestsFromName(f"{test_file}")
            suite.addTests(tests)
        except EOFError as e:
            raise Exception(f"Error loading tests from file {test_file}: {str(e)}")

    # Run the test suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    # Calculate the number of tests passed
    num_tests = result.testsRun
    num_tests_passed = num_tests - len(result.failures) - len(result.errors)

except Exception as e:
    print(f"Unit tests failed to run: {e}")
    sys.exit(1)

with open("num_tests.txt", "w") as file:
    file.write(str(num_tests))

with open("num_tests_passed.txt", "w") as file:
    file.write(str(num_tests_passed))
