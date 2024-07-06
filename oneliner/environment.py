from oneliner.token import Token
from oneliner.error import InterpretError
from typing import Self


class Environment:
    def __init__(self, enclosing: Self | None = None):
        self.variables = {}
        self.enclosing = enclosing

    def define(self, name: str, value):
        self.variables[name] = value

    def get_at(self, distance: int, name: str):
        env = self.ancestor(distance)
        assert name in env
        return env[name]

    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

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

    def assign_at(self, distance: int, name: Token, value):
        env = self.ancestor(distance)
        assert name.lexeme in env
        env[name.lexeme] = value
