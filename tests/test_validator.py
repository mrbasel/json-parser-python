import unittest
from jsonparser.parser import validator, Token, TokenType

class TestValidator(unittest.TestCase):
    def test_empty_object_valid(self):
        tokens = [Token(TokenType.symbol, "{"), Token(TokenType.symbol, "}")]
        self.assertTrue(validator(tokens))
    
    def test_empty_string_invalid(self):
        tokens = []
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

if __name__ == '__main__':
    unittest.main()
