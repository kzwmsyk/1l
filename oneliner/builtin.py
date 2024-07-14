from oneliner.function import Callable
from time import time
from oneliner.utll import camel_to_snake, stringify, is_truthy


def export_functions():
    return [Clock(), Print(), Str(), Float(), Int(), Bool(), Size()]


class NativeFunction(Callable):
    def name(self):
        return camel_to_snake(type(self).__name__)

    def alias(self) -> list[str]:
        return []


class NativeClass(Callable):
    def name(self):
        return type(self).__name__

    def alias(self) -> list[str]:
        return []


class Clock(NativeFunction):
    def arity(self):
        return 0

    def call(self, interpreter, arguments: list):
        return time()


class Print(NativeFunction):
    def arity(self):
        return 1

    def call(self, interpreter, arguments: list):
        print(stringify(arguments[0]))

    def alias(self):
        return ["p"]


class Str(NativeFunction):
    def arity(self):
        return 1

    def call(self, interpreter, arguments: list):
        return stringify(arguments[0])


class Float(NativeFunction):
    def arity(self):
        return 1

    def call(self, interpreter, arguments: list):
        return float(arguments[0])


class Int(NativeFunction):
    def arity(self):
        return 1

    def call(self, interpreter, arguments: list):
        return int(arguments[0])


class Bool(NativeFunction):
    def arity(self) -> Int:
        return 1

    def call(self, interpreter, arguments: list):
        return is_truthy(arguments[0])


class Size(NativeFunction):
    def arity(self) -> Int:
        return 1

    def call(self, interpreter, arguments: list):
        return len(arguments[0])

    def alias(self):
        return ["length", "len"]
