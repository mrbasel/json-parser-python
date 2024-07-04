import unittest
from jsonparser.parser import InvalidJson, validator, Token, TokenType

class TestValidator(unittest.TestCase):
    def test_empty_object_valid(self):
        tokens = [Token(TokenType.symbol, "{"), Token(TokenType.symbol, "}")]
        self.assertTrue(validator(tokens))
    
    def test_empty_string_invalid(self):
        tokens = []
        self.assertFalse(validator(tokens))
    
    def test_missing_closing_bracket_invalid(self):
        tokens = [            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            ]
        self.assertFalse(validator(tokens))

    def test_one_key_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, "}")
        ]
        self.assertTrue(validator(tokens))

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
        self.assertTrue(validator(tokens))

    def test_trailing_comma_invalid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, "value"),
            Token(TokenType.symbol, ","),
            Token(TokenType.symbol, "}")
        ]
        self.assertFalse(validator(tokens))

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
        self.assertFalse(validator(tokens))
    
    def test_multiple_data_types_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, True),
            Token(TokenType.symbol, ","),
            Token(TokenType.string, "key2"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, False),
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
            Token(TokenType.string, 101),
            Token(TokenType.symbol, "}")
        ]
        self.assertTrue(validator(tokens))


    def test_unkown_token_invalid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.string, True),
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
            Token(TokenType.string, 101),
            Token(TokenType.symbol, "}")
        ]
        self.assertFalse(validator(tokens))

    def test_array_value_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.array, []),
            Token(TokenType.symbol, "}")
        ]
        self.assertTrue(validator(tokens))

    def test_empty_array_valid(self):
        tokens = [Token(TokenType.symbol, "["), Token(TokenType.symbol, "]")]
        self.assertTrue(validator(tokens))

    def test_2d_array(self):
        tokens = [Token(TokenType.symbol, "["), Token(TokenType.symbol, "["), Token(TokenType.number, 2), Token(TokenType.symbol, "]"), Token(TokenType.symbol, "]")]
        self.assertTrue(validator(tokens))

    def test_array_value_valid(self):
        tokens = [
            Token(TokenType.symbol, "{"),
            Token(TokenType.string, "key1"),
            Token(TokenType.symbol, ":"),
            Token(TokenType.symbol, "["),
            Token(TokenType.symbol, "]"),
            Token(TokenType.symbol, "}")
        ]
        self.assertTrue(validator(tokens))

    def test_array_with_items_valid(self):
        tokens = [
            Token(TokenType.symbol, "["),
            Token(TokenType.number, 1),
            Token(TokenType.symbol, ","),
            Token(TokenType.number, 2),
            Token(TokenType.symbol, "]"),
        ]
        self.assertTrue(validator(tokens))


if __name__ == '__main__':
    unittest.main()
