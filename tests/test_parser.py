import unittest
from jsonparser.parser import parse, InvalidJson, Token, TokenType

class TestParser(unittest.TestCase):
    def test_empty_object_valid(self):
        tokens = [Token(TokenType.symbol, "{"), Token(TokenType.symbol, "}")]
        self.assertEqual(parse(tokens), {})
    
    def test_empty_string_invalid(self):
        tokens = []
        self.assertRaises(InvalidJson, parse, tokens)
    
    def test_missing_closing_bracket_invalid(self):
        tokens = [            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            ]
        self.assertRaises(InvalidJson, parse, tokens)

    def test_one_key_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, "}")
        ]
        self.assertEqual(parse(tokens), {"key": "value"})

    def test_two_key_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key2"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, "}")
        ]
        self.assertEqual(parse(tokens), {"key": "value", "key2": "value"})

    def test_trailing_comma_invalid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, ","),
            Token(TokenType.symbol, "}")
        ]
        self.assertRaises(InvalidJson, parse, tokens)

    def test_key_without_double_quotes_invalid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, ","),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, "}")
        ]
        self.assertRaises(InvalidJson, parse, tokens)
    
    def test_multiple_data_types_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.bool, True),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key2"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.bool, False),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key3"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "None"),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key4"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key5"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.number, 101),
            Token(TokenType.symbol, "}")
        ]
        self.assertEqual(parse(tokens), { "key1": True, "key2": False, "key3": "None", "key4": "value", "key5": 101 }
)


    def test_unknown_token_invalid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.bool, True),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key2"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.unknown, "False"),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key3"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, None),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key4"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key5"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.number, 101),
            Token(TokenType.symbol, "}")
        ]
        self.assertRaises(InvalidJson, parse, tokens)

    def test_empty_array_valid(self):
        tokens = [Token(TokenType.symbol, "["), Token(TokenType.symbol, "]")]
        self.assertEqual(parse(tokens), [])

    def test_2d_array(self):
        tokens = [Token(TokenType.symbol, "["), Token(TokenType.symbol, "["), Token(TokenType.number, 2), Token(TokenType.symbol, "]"), Token(TokenType.symbol, "]")]
        self.assertEqual(parse(tokens), [[2]])

    def test_array_with_items_valid(self):
        tokens = [
            Token(TokenType.symbol, "["),
            Token(TokenType.number, 1),
            Token(TokenType.symbol, ","),
            Token(TokenType.number, 2),
            Token(TokenType.symbol, "]"),
        ]
        self.assertEqual(parse(tokens), [1, 2])

    def test_empty_object_in_array_valid(self):
        tokens = [
            Token(TokenType.symbol, "["),
            Token(TokenType.symbol, "{"),
            Token(TokenType.symbol, "}"),
            Token(TokenType.symbol, "]"),
        ]
        self.assertEqual(parse(tokens), [{}])

    def test_object_in_array_valid(self):
        tokens = [
            Token(TokenType.symbol, "["),
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.number, 10),
            Token(TokenType.symbol, "}"),
            Token(TokenType.symbol, "]"),
        ]
        self.assertEqual(parse(tokens), [{"key1": 10}])

    def test_array_value_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.symbol, "["),
            Token(TokenType.symbol, "]"),
            Token(TokenType.symbol, "}")
        ]
        self.assertEqual(parse(tokens), {"key1": []})


if __name__ == '__main__':
    unittest.main()
