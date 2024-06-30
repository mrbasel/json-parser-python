from dataclasses import dataclass
from enum import Enum

TokenType = Enum("TokenType", ["symbol", "key", "string", "bool", "number", "null", "object", "array"])

@dataclass
class Token:
    type: TokenType
    value: any

class InvalidJson(Exception):
    pass

def tokeniser(text: str):
    tokens = []
    is_in_string = False
    string_token = ""

    for char in text:
        if char == "{" or char == "}" or char == ":" or char == ",":
            tokens.append(Token(TokenType.symbol, char))
        elif char == "\"" and not is_in_string:
            is_in_string = True
        elif char == "\"" and is_in_string:
            is_in_string = False
            tokens.append(Token(TokenType.string, string_token))
            string_token = ""
        elif is_in_string:
            string_token += char
        elif char == " ":
            continue
        else:
            raise InvalidJson()
    return tokens


def validator(tokens: list[Token]):
    if len(tokens) == 0:
        return False
    
    i = 0
    next_exp_token = "" # can be key, value, or bracket, colon, comma
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
        elif current_token.type == TokenType.string and "value" in next_exp_token:
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

    return True