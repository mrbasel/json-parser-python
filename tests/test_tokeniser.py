import unittest
from jsonparser.parser import tokeniser

class TestTokeniser(unittest.TestCase):
    def test_one_key(self):
        tokens = tokeniser(r'{"key": "value"}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", "value", "}"])

    def test_multiple_keys(self):
        tokens = tokeniser(r'{"key": "value", "key2": "value"}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", "value", ",", "key2", ":", "value", "}"])

    def test_int_value(self):
        tokens = tokeniser(r'{"key": 250}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", 250, "}"])

    def test_negative_number_value(self):
        tokens = tokeniser(r'{"key": -250}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", -250, "}"])

    def test_float_value(self):
        tokens = tokeniser(r'{"key": 10.4}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", 10.4, "}"])

    def test_bool_value(self):
        tokens = tokeniser(r'{"key": true}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", True, "}"])

    def test_null_value(self):
        tokens = tokeniser(r'{"key": null}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", None, "}"])

    def test_multiple_datatypes(self):
        tokens = tokeniser(r'{"key1": true, "key2": false, "key3": null, "key4": "value", "key5": 101}')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", True, ",", "key2", ":", False, ",", "key3", ":", None, ",",  "key4", ":", "value", ",", "key5", ":", 101, "}"])
    
    def test_empty_array(self):
        tokens = tokeniser(r'{"key1": [] }')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", "[", "]", "}"])

    def test_array_with_items(self):
        tokens = tokeniser(r'{"key1": [1, 2, 3] }')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", "[", 1, ",", 2, ",", 3, "]", "}"])

    def test_strings_with_newline(self):
        tokens = tokeniser(r'{"key1": "Hello\n" }')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", "Hello\\n", "}"])

    def test_inner_double_quote(self):
        tokens = tokeniser(r'{"key1": "\"Hello" }')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", "\"Hello", "}"])

    def test_fraction_less_than_one(self):
        tokens = tokeniser(r'{"key1": 0.5 }')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", 0.5, "}"])


