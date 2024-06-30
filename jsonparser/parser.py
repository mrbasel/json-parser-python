from dataclasses import dataclass
from enum import Enum

TokenType = Enum("TokenType", ["symbol", "string", "bool", "number", "null", "object", "array", "unknown"])

@dataclass
class Token:
    type: TokenType
    value: any

class InvalidJson(Exception):
    pass

def tokeniser(text: str):
    tokens = []

    i = 0
    while i < len(text):
        char = text[i]
        if char == "{" or char == "}" or char == ":" or char == ",":
            tokens.append(Token(TokenType.symbol, char))
        elif char == "\"":
            i += 1
            value = ""
            while i < len(text) and text[i] != "\"":
                value += text[i]
                i += 1
            tokens.append(Token(TokenType.string, value))
        elif char != " ":
            value = ""
            while i < len(text) and text[i] not in [" ", "{", "}", ":", ","]:
                value += text[i]
                i += 1
            if value == "true":
                tokens.append(Token(TokenType.bool, True))
            elif value == "false":
                tokens.append(Token(TokenType.bool, False))
            elif value == "null":
                tokens.append(Token(TokenType.null, None))
            elif value.isdigit():
                tokens.append(Token(TokenType.number, int(value)))
            else:
                tokens.append(Token(TokenType.unknown, value))
            i -= 1
        i += 1
    return tokens


def validator(tokens: list[Token]):
    if len(tokens) == 0:
        return False
    
    i = 0
    next_exp_token = [] # can contain key, value, or bracket, colon, comma
    while (i < len(tokens)): 
        current_token = tokens[i]
        if current_token.value == "{" and not next_exp_token:
            next_exp_token = ["key", "bracket"]
            i += 1
        elif current_token.type == TokenType.string and "key" in next_exp_token:
            next_exp_token = ["colon"]
            i += 1
        elif current_token.type == TokenType.symbol and current_token.value == ":" and "colon" in next_exp_token:
            next_exp_token = ["value"]
            i += 1
        elif current_token.type != TokenType.symbol and "value" in next_exp_token:
            if current_token.type == TokenType.unknown:
                return False
            next_exp_token = ["bracket", "comma"]
            i += 1
        elif current_token.type == TokenType.symbol and current_token.value == "," and "comma" in next_exp_token:
            next_exp_token = ["key"]
            i += 1
        elif current_token.value == "}" and "bracket" in next_exp_token:
            next_exp_token = []
            i += 1
        else:
            return False

    return len(next_exp_token) == 0