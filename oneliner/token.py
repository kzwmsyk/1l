from enum import Enum, auto
from typing import Union


class TokenType(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    DOUBLE_SLASH = auto()
    STAR = auto()
    QUESTION = auto()
    COLON = auto()

    HASH = auto()   # #
    PERCENT = auto()   # %
    PERCENT_LEFT_BRACE = auto()  # %{
    PIPE = auto()   # |
    DOUBLE_PIPE = auto()   # ||
    AMPERSAND = auto()   # &
    DOUBLE_AMPERSAND = auto()   # &&

    LAMBDA = auto()   # λ ^

    # TWO Character Token
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    DOUBLE_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # LITERAL
    IDENTIFIER = auto()
    STRING = auto()
    INT = auto()
    FLOAT = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    DO = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    METHOD = auto()
    NIL = auto()
    NOT = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    EOF = auto()


class Token:
    def __init__(self, type: TokenType,
                 lexeme: str,
                 literal: Union[int, float, str],
                 line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

    __repr__ = __str__
