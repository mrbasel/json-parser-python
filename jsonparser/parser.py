from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Generic

TokenType = Enum("TokenType", ["symbol", "string", "bool", "number", "null", "object", "unknown"])
T = TypeVar("T")

@dataclass
class Token(Generic[T]):
    type: TokenType
    value: T

class InvalidJson(Exception):
    pass

def tokeniser(text: str):
    tokens = []

    i = 0
    while i < len(text):
        char = text[i]
        if char == "{" or char == "}" or char == ":" or char == "," or char == "[" or char == "]":
            tokens.append(Token(TokenType.symbol, char))
        elif char == "\"":
            i += 1
            value = ""
            next_char_escaped = False
            while i < len(text):
                if text[i] == "\\" and next_char_escaped:
                    value += text[i]
                    next_char_escaped = False
                    i += 1
                elif text[i] == "\\" and not next_char_escaped:
                    if text[i + 1] != "\"":
                       value += text[i]
                    next_char_escaped = True
                    i += 1
                elif text[i] == "\"" and next_char_escaped:
                    value += text[i]
                    i += 1
                    next_char_escaped = False
                elif text[i] == "\"" and not next_char_escaped:
                    break
                else:
                    value += text[i]
                    i += 1
                    next_char_escaped = False

            tokens.append(Token(TokenType.string, value))
        elif char != " ":
            value = ""
            while i < len(text) and text[i] not in [" ", "{", "}", ":", ",", "[", "]"]:
                value += text[i]
                i += 1
            if value == "true":
                tokens.append(Token(TokenType.bool, True))
            elif value == "false":
                tokens.append(Token(TokenType.bool, False))
            elif value == "null":
                tokens.append(Token(TokenType.null, None))
            elif is_number(value):
                tokens.append(Token(TokenType.number, float(value)))
            elif value == "\n":
                continue
            else:
                tokens.append(Token(TokenType.unknown, value))
            i -= 1
        i += 1
    return tokens

def parse_object(tokens: list[Token]):
    res = {} 
    last_key = None
    i = 0
    next_exp_token = [] # can contain key, value, or bracket, colon, comma
    while (i < len(tokens)): 
        current_token = tokens[i]
        if current_token.value == "{" and not next_exp_token:
            next_exp_token = ["key", "}"]
            i += 1
        elif current_token.type == TokenType.string and "key" in next_exp_token:
            last_key = validate_string(current_token.value)
            next_exp_token = [":"]
            i += 1
        elif current_token.type == TokenType.symbol and current_token.value == ":" and ":" in next_exp_token:
            next_exp_token = ["value"]
            i += 1
        elif current_token.type == TokenType.symbol and "value" in next_exp_token and current_token.value == "[":
            start = i
            end = i
            level_counter = 0
            for char in tokens[i:]:
                if char.value == "[":
                    level_counter += 1
                elif char.value == "]":
                    level_counter -= 1
                if level_counter == 0:
                    break
                end += 1
            array_value = parse_array(tokens[start: end + 1])
            res[last_key] = array_value
            last_key = None
            next_exp_token = ["}", ","]
            i += (end - i + 1)

        elif current_token.type == TokenType.symbol and "value" in next_exp_token and current_token.value == "{":
            start = i
            end = i
            level_counter = 0
            for char in tokens[i:]:
                if char.value == "{":
                    level_counter += 1
                elif char.value == "}":
                    level_counter -= 1
                if level_counter == 0:
                    break
                end += 1
            obj_value = parse_object(tokens[start: end + 1])
            res[last_key] = obj_value
            last_key = None
            next_exp_token = ["}", ","]
            i += (end - i + 1)

        elif current_token.type != TokenType.symbol and "value" in next_exp_token:
            if current_token.type == TokenType.unknown:
                raise InvalidJson()
            if current_token.type == TokenType.string:
                res[last_key] = validate_string(current_token.value)
            else:
                res[last_key] = current_token.value
            last_key = None
            next_exp_token = ["}", ","]
            i += 1
        elif current_token.type == TokenType.symbol and current_token.value == "," and "," in next_exp_token:
            next_exp_token = ["key"]
            i += 1
        elif current_token.value == "}" and "}" in next_exp_token:
            next_exp_token = []
            i += 1
        else:
            raise InvalidJson()

    if len(next_exp_token) != 0:
        raise InvalidJson()
    return res

def parse_array(tokens: list[Token]):
    if len(tokens) == 0 or tokens[0].value != "[":
        raise InvalidJson()
    bracket_stack = [(t, i) for i, t in enumerate(tokens) if t.value in ["[", "]"]]
    res = []
    next_exp_token = ["value", "[", "]"] # comma, value, or bracket
    i = 1
    while (i < len(tokens)): 
        current_token = tokens[i]
        if current_token.value == "[" and "[" in next_exp_token:
            start = i
            end = i
            level_counter = 0
            for char in tokens[i:]:
                if char.value == "[":
                    level_counter += 1
                elif char.value == "]":
                    level_counter -= 1
                if level_counter == 0:
                    break
                end += 1
            res.append(parse_array(tokens[start: end + 1]))
            i += (end - i)
            next_exp_token = [",", "]"]
        elif current_token.type == TokenType.unknown:
            raise InvalidJson()
        elif current_token.value == "{" and "value" in next_exp_token:
            start = i
            end = i
            level_counter = 0
            for char in tokens[i:]:
                if char.value == "{":
                    level_counter += 1
                elif char.value == "}":
                    level_counter -= 1
                if level_counter == 0:
                    break
                end += 1
            res.append(parse_object(tokens[start: end + 1]))
            next_exp_token = [",", "]"]
            i += (end - i)
        elif current_token.value == "]" and "]" in next_exp_token:
            next_exp_token = []
        elif current_token.type != TokenType.symbol and "value" in next_exp_token:
            if current_token.type == TokenType.string:
                res.append(validate_string(current_token.value))
            else:
                res.append(current_token.value)
            next_exp_token = [",", "]"]
        elif current_token.type == TokenType.symbol and current_token.value == "," and "," in next_exp_token:
            next_exp_token = ["value", "["]
        else:
            raise InvalidJson()
        i += 1

    if (len(bracket_stack) % 2) == 0 and len(next_exp_token) == 0:
        return res
    raise InvalidJson()

def parse(tokens: list[Token]):
    if len(tokens) == 0:
        raise InvalidJson()
    elif tokens[0].value == "[":
        return parse_array(tokens)
    elif tokens[0].value == "{":
        return parse_object(tokens)
    else:
        raise InvalidJson()

def validator(tokens: list[Token]):
    try:
        parse(tokens)
        return True
    except InvalidJson:
        return False

def load(text: str):
    tokens = tokeniser(text)
    return parse(tokens)

def is_number(input_string: str):
    try:
        # check if leading zero and number is not equal to zero (eg. 012)
        if len(input_string) > 0 and input_string[0] == "0" and float(input_string) != 0 and "." not in input_string:
            return False
        float(input_string)
        return True
    except ValueError:
        return False

def validate_string(input_string: str):
    if "\n" in input_string:
        raise InvalidJson(f"Invalid linebreak in {input_string}")
    if "\t" in input_string:
        raise InvalidJson(f"Invalid tab in {input_string}")

    repr_string = repr(input_string)[1:-1]
    i = 0
    while i < len(repr_string):
        if repr_string[i] == "\\" and ((i + 1) < len(repr_string) and repr_string[i + 1] not in ["'", "\"", "\\", "/", "b", "f", "n", "r", "t", "u"]):
            raise InvalidJson(f"Invalid escape sequence \\{repr_string[i+1]}")
        i += 1

    return repr_string
