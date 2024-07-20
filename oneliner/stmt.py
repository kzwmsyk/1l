from oneliner.token import Token
from oneliner.expr import Expr, VariableExpr, FunctionExpr
from abc import ABC, abstractmethod


class Stmt:
    def accept(self, visitor):
        pass


class BlockStmt(Stmt):
    def __init__(self,
                 statements: list[Stmt]):

        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


class EmptyStmt(Stmt):
    def __init__(self,
                 semicolon: Token):

        self.semicolon = semicolon

    def accept(self, visitor):
        return visitor.visit_empty_stmt(self)


class ExpressionStmt(Stmt):
    def __init__(self,
                 expression: Expr):

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


class FunctionStmt(Stmt):
    def __init__(self,
                 name: Token,
                 function: FunctionExpr):

        self.name = name
        self.function = function

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)


class ClassStmt(Stmt):
    def __init__(self,
                 name: Token,
                 superclass: VariableExpr,
                 methods: list[FunctionStmt]):

        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visit_class_stmt(self)


class IfStmt(Stmt):
    def __init__(self,
                 condition: Expr,
                 then_branch: Stmt,
                 else_branch: Stmt):

        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


class ReturnStmt(Stmt):
    def __init__(self,
                 keyword: Token,
                 value: Expr):

        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


class VarStmt(Stmt):
    def __init__(self,
                 name: Token,
                 initializer: Expr):

        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)


class WhileStmt(Stmt):
    def __init__(self,
                 condition: Expr,
                 body: Stmt):

        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


class StmtVisitor(ABC):

    @abstractmethod
    def visit_block_stmt(self, stmt: BlockStmt):
        pass

    @abstractmethod
    def visit_empty_stmt(self, stmt: EmptyStmt):
        pass

    @abstractmethod
    def visit_expression_stmt(self, stmt: ExpressionStmt):
        pass

    @abstractmethod
    def visit_function_stmt(self, stmt: FunctionStmt):
        pass

    @abstractmethod
    def visit_class_stmt(self, stmt: ClassStmt):
        pass

    @abstractmethod
    def visit_if_stmt(self, stmt: IfStmt):
        pass

    @abstractmethod
    def visit_return_stmt(self, stmt: ReturnStmt):
        pass

    @abstractmethod
    def visit_var_stmt(self, stmt: VarStmt):
        pass

    @abstractmethod
    def visit_while_stmt(self, stmt: WhileStmt):
        pass
