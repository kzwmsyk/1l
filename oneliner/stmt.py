from oneliner.token import Token
from oneliner.expr import VariableExpr
from oneliner.expr import Expr


class Stmt:
    # Visitor Interface
    # class Visitor<R>:
    #     R visit_foo_stmt(Foo stmt)
    #     R visit_bar_expr(Bar expr)

    def accept(visitor):
        pass


class BlockStmt(Stmt):
    statements: list[Stmt]

    def __init__(self,
                 statements: list[Stmt]):

        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)


class ExpressionStmt(Stmt):
    expression: Expr

    def __init__(self,
                 expression: Expr):

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)


class FunctionStmt(Stmt):
    name: Token
    params: list[Token]
    body: list[Stmt]

    def __init__(self,
                 name: Token,
                 params: list[Token],
                 body: list[Stmt]):

        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function_stmt(self)


class ClassStmt(Stmt):
    name: Token
    superclass: VariableExpr
    methods: list[FunctionStmt]

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
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt

    def __init__(self,
                 condition: Expr,
                 then_branch: Stmt,
                 else_branch: Stmt):

        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


class PrintStmt(Stmt):
    expression: Expr

    def __init__(self,
                 expression: Expr):

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)


class ReturnStmt(Stmt):
    keyword: Token
    value: Expr

    def __init__(self,
                 keyword: Token,
                 value: Expr):

        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_return_stmt(self)


class VarStmt(Stmt):
    name: Token
    initializer: Expr

    def __init__(self,
                 name: Token,
                 initializer: Expr):

        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)


class WhileStmt(Stmt):
    condition: Expr
    body: Stmt

    def __init__(self,
                 condition: Expr,
                 body: Stmt):

        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)
