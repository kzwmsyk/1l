import re
from oneliner.token import Token, TokenType
from typing import Union
from oneliner.error import ErrorReporter

keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "cls": TokenType.CLASS,
    "do": TokenType.DO,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "f": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "fn": TokenType.FUN,
    "if": TokenType.IF,
    "method": TokenType.METHOD,
    "mthd": TokenType.METHOD,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "p": TokenType.PRINT,
    "print": TokenType.PRINT,
    "not":  TokenType.NOT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "t": TokenType.TRUE,
    "var": TokenType.VAR,
    "v": TokenType.VAR,
    "while": TokenType.WHILE
}


class Scanner:

    def __init__(self, source: str, error_reporter: ErrorReporter):
        self.tokens = []
        self.source = source
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.error_reporter = error_reporter

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        char = self.advance()

        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "?":
                self.add_token(TokenType.QUESTION)
            case ":":
                self.add_token(TokenType.COLON)

            case "!":
                self.add_token(TokenType.BANG_EQUAL
                               if self.match("=")
                               else TokenType.BANG)
            case "=":
                self.add_token(TokenType.DOUBLE_EQUAL
                               if self.match("=")
                               else TokenType.EQUAL)
            case "<":
                self.add_token(TokenType.LESS_EQUAL
                               if self.match("=")
                               else TokenType.LESS)
            case ">":
                self.add_token(TokenType.GREATER_EQUAL
                               if self.match("=")
                               else TokenType.GREATER)

            case "&":
                self.add_token(TokenType.DOUBLE_AMPERSAND
                               if self.match("&")
                               else TokenType.AMPERSAND)
            case "|":
                self.add_token(TokenType.DOUBLE_PIPE
                               if self.match("|")
                               else TokenType.PIPE)
            case "%":
                self.add_token(TokenType.PERCENT)
            case "#":
                # コメント
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            case "/":
                self.add_token(TokenType.DOUBLE_SLASH
                               if self.match("/")
                               else TokenType.SLASH)
            case " " | "\t" | "\r":
                pass
            case "\n":
                self.line += 1
            case '"' | "'":
                self.string(char)
            case _:
                if self.is_digit(char):
                    self.number()
                elif self.is_alpha(char):
                    self.identifier()
                else:
                    self.error_reporter.error(
                        self.line, f"Unknown character: {char}"
                    )

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        char = self.source[self.current]
        self.current += 1
        return char

    def match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current+1]

    def add_token(self,
                  type: TokenType,
                  literal: Union[int, float, str, None] = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def string(self, closer: str):
        while self.peek() != closer and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error_reporter.error(self.line, "Unterminated string")
            return

        self.advance()  # 閉じる引用符を消費
        self.add_token(TokenType.STRING,
                       self.source[self.start + 1:self.current - 1])

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        is_float = False
        # 小数点
        if self.peek() == "." and self.is_digit(self.peek_next()):
            # 小数点を消費
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
            is_float = True

        number_text = self.source[self.start:self.current]

        if is_float:
            self.add_token(TokenType.FLOAT, float(number_text))
        else:
            self.add_token(TokenType.INT, int(number_text))

    def is_digit(self, char: str):
        return bool(re.match(r'^[0-9]$', char))

    def is_alpha(self, char: str):
        return bool(re.match(r'^[A-Za-z_]$', char))

    def is_alpha_numeric(self, char: str):
        return self.is_alpha(char) or self.is_digit(char)

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        identifier_text = self.source[self.start:self.current]

        if identifier_text in keywords:
            self.add_token(keywords[identifier_text])
        else:
            self.add_token(TokenType.IDENTIFIER)
