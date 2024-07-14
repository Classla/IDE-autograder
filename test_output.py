import unittest
import TestMyModule as test_module


def count_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(test_module)

    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    total_tests = result.testsRun
    passed_tests = total_tests - len(result.failures) - len(result.errors)

    if total_tests == 0:
        fraction_passed = 0
    else:
        fraction_passed = passed_tests / total_tests

    print(f"Total tests: {total_tests}")
    print(f"Passed tests: {passed_tests}")
    print(f"Fraction passed: {fraction_passed:.2f}")
