import unittest
from jsonparser.parser import validator

class TestValidator(unittest.TestCase):
    def test_empty_object_valid(self):
        tokens = [{"type": "symbol", "value": "{"}, {"type": "symbol", "value": "}"}]
        self.assertTrue(validator(tokens))
    
    def test_empty_string_invalid(self):
        tokens = []
        self.assertFalse(validator(tokens))

    def test_one_key_valid(self):
        tokens = [{'type': 'symbol', 'value': '{'}, {'type': 'string', 'value': 'key'}, {'type': 'symbol', 'value': ':'}, {'type': 'string', 'value': 'value'}, {'type': 'symbol', 'value': '}'}]
        self.assertTrue(validator(tokens))

    def test_two_key_valid(self):
        tokens = [{'type': 'symbol', 'value': '{'}, {'type': 'string', 'value': 'key'}, {'type': 'symbol', 'value': ':'}, {'type': 'string', 'value': 'value'}, {'type': 'symbol', 'value': ','}, {'type': 'string', 'value': 'key2'}, {'type': 'symbol', 'value': ':'}, {'type': 'string', 'value': 'value'}, {'type': 'symbol', 'value': '}'}]
        self.assertTrue(validator(tokens))

    def test_trailing_comma_invalid(self):
        tokens = [{'type': 'symbol', 'value': '{'}, {'type': 'string', 'value': 'key'}, {'type': 'symbol', 'value': ':'}, {'type': 'string', 'value': 'value'}, {'type': 'symbol', 'value': ','}, {'type': 'symbol', 'value': '}'}]
        self.assertFalse(validator(tokens))

    def test_key_without_double_quotes_invalid(self):
        tokens = [{'type': 'symbol', 'value': '{'}, {'type': 'string', 'value': 'key'}, {'type': 'symbol', 'value': ':'}, {'type': 'string', 'value': 'value'}, {'type': 'symbol', 'value': ','}, {'type': 'symbol', 'value': ':'}, {'type': 'string', 'value': 'value'}, {'type': 'symbol', 'value': '}'}]
        self.assertFalse(validator(tokens))

# if __name__ == '__main__':
#     unittest.main()
