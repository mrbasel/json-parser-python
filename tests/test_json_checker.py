import unittest, os
from jsonparser.parser import validator, tokeniser

class TestJsonCheckerCases(unittest.TestCase):
    def test_all_cases(self):
        test_files = os.listdir("tests/json_checker_tests")
        tests = []
        for file in test_files:
            if file.startswith("fail") or file.startswith("pass"):
                with open(f"tests/json_checker_tests/{file}") as f:
                    tests.append((file, f.read()))

        for test in tests:
            with self.subTest(file=test[0]):
                if test[0].startswith("fail"):
                    self.assertFalse(validator(tokeniser(test[1])))
                else:
                    self.assertTrue(validator(tokeniser(test[1])))
