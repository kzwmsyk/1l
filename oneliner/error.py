from oneliner.token import Token, TokenType


class ErrorReporter():
    def __init__(self):
        self.has_error = False
        self.has_runtime_error = False

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def token_error(self, token: Token, message: str):
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def runtime_error(self, error: RuntimeError):
        print(f"[line:{error.token.line}] Runtime error: {error.message}")
        self.has_runtime_error = True

    def report(self, line: int, where: str, message: str):
        print(f"Error on line {line} {where}: {message}")
        self.has_error = True

    def reset(self):
        self.has_error = False
        self.has_runtime_error = False


class ScanError(Exception):
    def __init__(self, ｃhar: str, message: str, line: int, current: int):
        super().__init__(message)

        self.char = char
        self.line = line
        self.current = current
        self.message = message + f"({char})"


class ParseError(Exception):
    pass


class InterpretError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message
