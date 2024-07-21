import unittest

# List of test filenames (without the .py extension)
test_files = [
    "tests.test_main",
    "tests.test_another",  # Add other test files here
]

# Create a test suite
suite = unittest.TestSuite()

# Load tests from each test file
loader = unittest.TestLoader()
for test_file in test_files:
    suite.addTests(loader.loadTestsFromName(test_file))

# Run the test suite
runner = unittest.TextTestRunner()
result = runner.run(suite)

# Calculate the number of tests passed
num_tests_run = result.testsRun
num_tests_failed = len(result.failures) + len(result.errors)
num_tests_passed = num_tests_run - num_tests_failed

print(f"Number of tests passed: {num_tests_passed}")
