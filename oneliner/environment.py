from oneliner.token import Token
from oneliner.error import InterpretError
from typing import Self


class Environment:
    def __init__(self, enclosing: Self | None = None):
        self.variables = {}
        self.enclosing = enclosing

    def define(self, name: str, value):
        self.variables[name] = value

    def get(self, name: Token):
        if name.lexeme in self.variables:
            return self.variables[name.lexeme]
        elif self.enclosing is not None:
            return self.enclosing.get(name)
        else:
            raise InterpretError(name, f"Undefined variable: '{name.lexeme}'")

    def assign(self, name: Token, value):

        if name.lexeme in self.variables:
            self.variables[name.lexeme] = value
            return
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        else:
            raise InterpretError(name, f"Undefined variable: '{name.lexeme}'")
