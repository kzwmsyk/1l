from oneliner.token import Token
from oneliner.function import Function, Callable
from oneliner.expr import Expr
from oneliner.error import InterpretError


class Klass(Callable):
    def __init__(self, name: Token, methods: dict[str, Function]):
        self.name = name
        self.methods = methods

    def __str__(self):
        return f"<class {self.name}>"

    def find_method(self, name: str) -> Function | None:
        if name in self.methods:
            return self.methods[name]
        return None

    def call(self, interpreter, arguments: list[Expr]):
        instance: Instance = Instance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()


class Instance():
    def __init__(self, klass: Klass):
        self.klass = klass
        self.fields = {}

    def __str__(self) -> str:
        return f"<instance of {self.klass.name}>"

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)

        if method is not None:
            return method.bind(self)

        raise InterpretError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value):
        self.fields[name.lexeme] = value
