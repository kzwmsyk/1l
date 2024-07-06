from oneliner.error import ErrorReporter
from oneliner.token import Token
from oneliner.interpreter import Interpreter
from oneliner.expr import AssignExpr, BinaryExpr, Expr, SetExpr, TernaryExpr, \
    VariableExpr, CallExpr, GroupingExpr, LiteralExpr, LogicalExpr, \
    UnaryExpr, GetExpr, ThisExpr
from oneliner.stmt import BlockStmt, IfStmt, PrintStmt, Stmt, VarStmt, \
    FunctionStmt, ExpressionStmt, ReturnStmt, WhileStmt, ClassStmt
from enum import Enum, auto


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    METHOD = auto()
    INITIALIZER = auto()


class Resolver():
    def __init__(self,
                 interpreter: Interpreter,
                 error_reporter: ErrorReporter):
        self.interpreter = interpreter
        self.error_reporter = error_reporter
        self.scopes: list[dict[str, bool]] = []
        self.current_function = FunctionType.NONE

    def resolve(self, obj) -> None:
        if isinstance(obj, Expr):
            self.resolve_expression(obj)
        elif isinstance(obj, Stmt):
            self.resolve_statement(obj)
        elif isinstance(obj, list):
            self.resolve_statements(obj)

    def resolve_expression(self, expr: Expr) -> None:
        expr.accept(self)

    def resolve_statement(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def resolve_statements(self, stmts: list[Stmt]):
        for stmt in stmts:
            self.resolve(stmt)

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_class_stmt(self, stmt: ClassStmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.begin_scope()
        self.scopes[-1]["this"] = True

        for method in stmt.methods:
            self.resolve_function(method, FunctionType.METHOD)

        self.end_scope()

    def begin_scope(self) -> None:
        scope: dict[str, bool] = {}
        self.scopes.append(scope)

    def end_scope(self) -> None:
        self.scopes.pop()

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def declare(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.error_reporter.error(name, "Can't redeclare variable.")
            return

        scope[name.lexeme] = False

    def define(self, name: Token) -> None:
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def visit_variable_expr(self, expr: VariableExpr) -> None:
        if (len(self.scopes) > 0) \
                and (expr.name.lexeme in self.scopes[-1]) \
                and (self.scopes[-1][expr.name.lexeme] is False):
            self.error_reporter.error(
                expr.name,
                "Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)

    def resolve_local(self, expr: Expr, name: Token) -> None:
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def visit_assign_expr(self, expr: AssignExpr) -> None:
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_function_stmt(self, stmt: FunctionStmt) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)

    def resolve_function(self,
                         function: FunctionStmt,
                         type: FunctionType) -> None:
        enclosing_function = self.current_function
        self.current_function = type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()

        self.current_function = enclosing_function

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self.resolve(stmt.expression)

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        self.resolve(stmt.expression)

    def visit_return_stmt(self, stmt: ReturnStmt) -> None:
        if self.current_function == FunctionType.NONE:
            self.error_reporter.error(
                stmt.keyword,
                "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve(stmt.value)

    def visit_while_stmt(self, stmt: WhileStmt) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_binary_expr(self, expr: BinaryExpr) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_ternary_expr(self, expr: TernaryExpr) -> None:
        self.resolve(expr.condition)
        self.resolve(expr.then_expr)
        self.resolve(expr.else_expr)

    def visit_call_expr(self, expr: CallExpr) -> None:
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)

    def visit_get_expr(self, expr: GetExpr) -> None:
        self.resolve(expr.object)

    def visit_set_expr(self, expr: SetExpr) -> None:
        self.resolve(expr.value)
        self.resolve(expr.object)

    def visit_grouping_expr(self, expr: GroupingExpr) -> None:
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr) -> None:
        pass

    def visit_logical_expr(self, expr: LogicalExpr) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_unary_expr(self, expr: UnaryExpr) -> None:
        self.resolve(expr.operand)

    def visit_this_expr(self, expr: ThisExpr) -> None:
        self.resolve_local(expr, expr.keyword)
