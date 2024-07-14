from oneliner.klass import Instance, Klass
from oneliner.token import TokenType, Token
from oneliner.expr import Expr, LiteralExpr, GroupingExpr, SetExpr, \
    BinaryExpr, SuperExpr, TernaryExpr, VariableExpr, AssignExpr, \
    LogicalExpr, CallExpr, GetExpr, ThisExpr, UnaryExpr, FunctionExpr
from oneliner.stmt import Stmt, ExpressionStmt, VarStmt, \
    BlockStmt, IfStmt, WhileStmt, FunctionStmt, ReturnStmt, ClassStmt
from oneliner.error import InterpretError, ErrorReporter, Return
from oneliner.environment import Environment
from oneliner.function import Function, Callable, Partial
from oneliner.builtin import NativeFunction, export_functions
from oneliner.utll import stringify, is_truthy
from typing import Self

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Interpreter:
    # ExprVisitor, StmtVisitor
    globals = Environment()

    def __init__(self, error_reporter: ErrorReporter):
        self.environment = Interpreter.globals
        self.locals = {}
        self.error_reporter = error_reporter
        self.register_natives(export_functions())

    def register_natives(self, natives: list[NativeFunction]):
        for native in natives:
            self.globals.define(native.name(), native)

            for alias in native.alias():
                self.globals.define(alias, native)

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except InterpretError as e:
            self.error_reporter.runtime_error(e)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

    def visit_return_stmt(self, stmt: ReturnStmt) -> None:
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self.evaluate(stmt.expression)

    def visit_function_stmt(self, stmt: FunctionStmt) -> None:
        function = Function(stmt=stmt,
                            closure=self.environment,
                            is_initializer=False)
        self.environment.define(stmt.name.lexeme, function)

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        self.execute_block(stmt.statements, Environment(self.environment))

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous: Environment = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_function_expr(self, expr: FunctionExpr) -> None:
        return Function(expr=expr,
                        closure=self.environment,
                        is_initializer=False)

    def visit_class_stmt(self, stmt: ClassStmt):
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, Klass):
                raise InterpretError(stmt.superclass.name,
                                     "Superclass must be a class.")

        self.environment.define(stmt.name.lexeme, None)
        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods = {}
        for method in stmt.methods:
            function = Function(
                stmt=method,
                closure=self.environment,
                is_initializer=method.name.lexeme == "init")
            methods[method.name.lexeme] = function

        klass = Klass(stmt.name, superclass, methods)

        if superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, klass)

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        if is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: WhileStmt) -> None:
        while is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_assign_expr(self, expr: AssignExpr):
        value = self.evaluate(expr.value)

        distance = self.locals.get(expr, None)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.environment.assign(expr.name, value)

        return value

    def visit_literal_expr(self, expr: LiteralExpr):
        return expr.value

    def visit_grouping_expr(self, expr: GroupingExpr):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: UnaryExpr):
        operand = self.evaluate(expr.operand)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_numeric_operand(expr.operator, operand)
                return - operand
            case TokenType.NOT | TokenType.BANG:
                return not is_truthy(operand)
            case _:
                raise InterpretError(expr.operator, "Unreachable")

    def check_numeric_operand(self, operator: Token, operand):
        if not self.is_numeric(operand):
            raise InterpretError(operator, "Operand must be number")

    def check_numeric_operands(self, operator: Token, left, right):
        if not (self.is_numeric(left) and self.is_numeric(right)):
            raise InterpretError(operator, "Operands must be numbers")

    def is_numeric(self, object):
        return isinstance(object, float) or isinstance(object, int)

    def visit_ternary_expr(self, expr: TernaryExpr):
        condition = self.evaluate(expr.condition)
        if is_truthy(condition):
            return self.evaluate(expr.then_expr)
        else:
            return self.evaluate(expr.else_expr)

    def visit_logical_expr(self, expr: LogicalExpr):
        left = self.evaluate(expr.left)

        match expr.operator.type:
            case TokenType.OR | TokenType.DOUBLE_PIPE:
                if is_truthy(left):
                    return left
            case TokenType.AND | TokenType.DOUBLE_AMPERSAND:
                if not is_truthy(left):
                    return left

        return self.evaluate(expr.right)

    def visit_binary_expr(self, expr: BinaryExpr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.PLUS:
                if self.is_numeric(left) and self.is_numeric(right):
                    return left + right
                else:
                    return stringify(left) + stringify(right)
            case TokenType.MINUS:
                self.check_numeric_operands(expr.operator, left, right)
                return left - right
            case TokenType.STAR:
                self.check_numeric_operands(expr.operator, left, right)
                return left * right
            case TokenType.SLASH:
                self.check_numeric_operands(expr.operator, left, right)
                return left / right
            case TokenType.DOUBLE_SLASH:
                return left // right
            case TokenType.PERCENT:
                self.check_numeric_operands(expr.operator, left, right)
                return left % right
            case TokenType.GREATER:
                self.check_numeric_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_numeric_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_numeric_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_numeric_operands(expr.operator, left, right)
                return left <= right
            case TokenType.DOUBLE_EQUAL:
                return self.is_equal(left, right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case _:
                raise InterpretError(expr.operator, "Unreachable")

    def is_equal(self, left, right):
        if left is None and right is None:
            return True
        if left is None:
            return False
        return left == right

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visit_variable_expr(self, expr: VariableExpr):
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name: Token, expr: Expr):
        distance = self.locals.get(expr, None)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        return self.globals.get(name)

    def visit_call_expr(self, expr: CallExpr):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(arg) for arg in expr.arguments]
        if not isinstance(callee, Callable):
            raise InterpretError(
                expr.paren, "Can only callable functions and classes.")

        if len(arguments) != callee.arity():
            raise InterpretError(
                expr.paren,
                f"Expected {callee.arity()} arguments but got {
                    len(arguments)}."
            )
        return callee.call(self, arguments)

    def visit_get_expr(self, expr: GetExpr):
        "foo.bar"

        invocant = self.evaluate(expr.object)
        property = expr.name

        if isinstance(invocant, Instance):
            return invocant.get(property)

        # syntax sugar: obj.foo(x,y,z) == foo(obj, x,y,z)
        # resolve dynamic
        function = self.environment.get(property)
        if function is not None and isinstance(function, Callable):
            if function.arity() < 1:
                raise InterpretError(
                    property,
                    "Callable must have at least 1 argument")
            return Partial(function, invocant)

        raise InterpretError(property,
                             "Neither instance property nor callable")

    def visit_set_expr(self, expr: SetExpr):
        object = self.evaluate(expr.object)
        if not isinstance(object, Instance):
            raise InterpretError(expr.name,
                                 "Only instances have fields.")

        value = self.evaluate(expr.value)
        object.set(expr.name, value)
        return value

    def visit_this_expr(self, expr: ThisExpr):
        return self.look_up_variable(expr.keyword, expr)

    def visit_super_expr(self, expr: SuperExpr):
        distance = self.locals.get(expr, None)
        superclass = self.environment.get_at(distance, "super")
        object = self.environment.get_at(distance - 1, "this")

        method = superclass.find_method(expr.method.lexeme)
        if method is None:
            raise InterpretError(expr.method,
                                 f"Undefined property '{expr.method.lexeme}'.")
        return method.bind(object)
