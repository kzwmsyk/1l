from oneliner.function import Callable
from time import time
from oneliner.utll import camel_to_snake


class NativeFunction(Callable):
    def name(self):
        return camel_to_snake(type(self).__name__)


class NativeClass(Callable):
    def name(self):
        return type(self).__name__


class Clock(NativeFunction):
    def arity(self):
        return 0

    def call(self, interpreter, arguments: list):
        return time()


class PPrint(NativeFunction):
    def arity(self):
        return 1

    def call(self, interpreter, arguments: list):
        print(arguments[0])


class List(NativeClass):
    pass


class Map(NativeClass):
    pass
