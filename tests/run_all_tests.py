import unittest

from tests.test_handwriting_recognition import TestHandwritingRecognition
from tests.test_file_handler import TestFileHandler


def run_listed_tests():
    """
    Run all test lited below.
    """

    # set of test classes
    test_classes_to_run = [TestHandwritingRecognition, TestFileHandler]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    test_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    runner.run(test_suite)


def run_all_tests():  # run all test
    """
    Run all test.
    """

    loader = unittest.TestLoader()
    test_suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(test_suite)


if __name__ == '__main__':
    run_all_tests()
    # run_listed_tests()