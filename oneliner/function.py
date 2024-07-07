from oneliner.expr import FunctionExpr
from oneliner.stmt import FunctionStmt
from oneliner.environment import Environment
from abc import ABC, abstractmethod
from oneliner.error import Return
from oneliner.token import Token


class Callable(ABC):
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments: list):
        pass


class Function(Callable):
    def __init__(self,
                 stmt: FunctionStmt | None = None,
                 name: Token | None = None,
                 expr: FunctionExpr | None = None,
                 closure: Environment = None,
                 is_initializer: bool = False):
        if stmt is not None:
            self.name = stmt.name
            self.expr = stmt.function
        else:
            self.name = name
            self.expr = expr
        self.closure: Environment = closure
        self.is_initializer = is_initializer

    def arity(self) -> int:
        return len(self.expr.params)

    def call(self, interpreter, arguments: list):
        environment: Environment = Environment(self.closure)
        for i in range(len(self.expr.params)):
            environment.define(
                self.expr.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.expr.body, environment)
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value

        if self.is_initializer:
            return self.closure.get_at(0, "this")

        return None

    def bind(self, instance):
        environment: Environment = Environment(self.closure)
        environment.define("this", instance)
        return Function(name=self.name,
                        expr=self.expr,
                        closure=environment,
                        is_initializer=self.is_initializer)

    def __str__(self):
        return f"<fun {self.name.lexeme}>" if self.name else "<lambda>"
