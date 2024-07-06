from oneliner.stmt import FunctionStmt
from oneliner.environment import Environment
from abc import ABC, abstractmethod
from oneliner.error import Return


class Callable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: list):
        pass


class Function(Callable):
    def __init__(self, declaration: FunctionStmt, closure: Environment):
        self.declaration: FunctionStmt = declaration
        self.closure: Environment = closure

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments: list):
        environment: Environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(
                self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None

    def bind(self, instance):
        environment: Environment = Environment(self.closure)
        environment.define("this", instance)
        return Function(self.declaration, environment)

    def __str__(self):
        return "<fun " + self.declaration.name.lexeme + ">"
