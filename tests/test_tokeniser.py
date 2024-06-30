import unittest
from jsonparser.parser import tokeniser, InvalidJson

class TestTokeniser(unittest.TestCase):
    def test_one_key(self):
        tokens = tokeniser("{\"key\": \"value\"}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", "value", "}"])

    def test_multiple_keys(self):
        tokens = tokeniser("{\"key\": \"value\", \"key2\": \"value\"}")
        self.assertEqual(list(map(lambda t: t.value, tokens)), ["{", "key", ":", "value", ",", "key2", ":", "value", "}"])

    def test_missing_quote_raises_error(self):
        test_string = "{\"key: \"value\"}"
        self.assertRaises(InvalidJson, tokeniser, test_string)


    
    

if __name__ == '__main__':
    unittest.main()