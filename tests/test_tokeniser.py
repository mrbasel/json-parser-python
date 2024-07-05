import unittest
from jsonparser.parser import tokeniser

class TestTokeniser(unittest.TestCase):
    def test_one_key(self):
        tokens = tokeniser("{\"key\": \"value\"}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", "value", "}"])

    def test_multiple_keys(self):
        tokens = tokeniser("{\"key\": \"value\", \"key2\": \"value\"}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", "value", ",", "key2", ":", "value", "}"])

    def test_int_value(self):
        tokens = tokeniser("{\"key\": 250}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", 250, "}"])

    def test_negative_number_value(self):
        tokens = tokeniser("{\"key\": -250}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", -250, "}"])

    def test_float_value(self):
        tokens = tokeniser("{\"key\": 10.4}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", 10.4, "}"])

    def test_bool_value(self):
        tokens = tokeniser("{\"key\": true}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", True, "}"])

    def test_null_value(self):
        tokens = tokeniser("{\"key\": null}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", None, "}"])

    def test_multiple_datatypes(self):
        tokens = tokeniser("{\"key1\": true, \"key2\": false, \"key3\": null, \"key4\": \"value\", \"key5\": 101}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", True, ",", "key2", ":", False, ",", "key3", ":", None, ",",  "key4", ":", "value", ",", "key5", ":", 101, "}"])
    
    def test_empty_array(self):
        tokens = tokeniser("{\"key1\": [] }")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", "[", "]", "}"])

    def test_array_with_items(self):
        tokens = tokeniser("{\"key1\": [1, 2, 3] }")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", "[", 1, ",", 2, ",", 3, "]", "}"])

    def test_strings_with_newline(self):
        tokens = tokeniser('{\"key1\": "Hello\n" }')
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key1", ":", "Hello\n", "}"])
