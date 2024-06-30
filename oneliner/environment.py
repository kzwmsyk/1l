from oneliner.token import Token
from oneliner.error import InterpretError


class Environment:
    def __init__(self):
        self.variables = {}

    def define(self, name: str, value):
        self.variables[name] = value

    def get(self, name: Token):
        if name.lexeme in self.variables:
            return self.variables[name.lexeme]
        else:
            raise InterpretError(name, f"Undefined variable: '{name.lexeme}'")

    def assign(self, name: Token, value):
        if name.lexeme not in self.variables:
            raise InterpretError(name, f"Undefined variable: '{name.lexeme}'")
        self.variables[name.lexeme] = value

    def set_variable(self, name, value):
        self.variables[name] = value
