from oneliner.function import Callable
from time import time
from oneliner.utll import camel_to_snake, stringify


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


class List(NativeClass):
    pass


class Map(NativeClass):
    pass
