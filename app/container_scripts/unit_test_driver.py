"""This script is for the container. It is not to be run in app."""

# pylint: disable=import-error

import inspect
import unittest
import unit_tests  # type: ignore


def count_tests(class_ref):
    """_summary_"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(class_ref)

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


if __name__ == "__main__":
    class_names = [
        name for name, obj in inspect.getmembers(unit_tests) if inspect.isclass(obj)
    ]

    if len(class_names) == 0:
        raise ValueError("No test classes detected.")

    for class_name in class_names:
        count_tests(getattr(unit_tests, class_name))
