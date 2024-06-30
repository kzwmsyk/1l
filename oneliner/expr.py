from oneliner.token import Token


class Expr:
    # Visitor Interface
    # class Visitor<R>:
    #     R visit_foo_stmt(Foo stmt)
    #     R visit_bar_expr(Bar expr)

    def accept(visitor):
        pass


class AssignExpr(Expr):
    name: Token
    value: Expr

    def __init__(self,
                 name: Token,
                 value: Expr):

        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __init__(self,
                 left: Expr,
                 operator: Token,
                 right: Expr):

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class CallExpr(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

    def __init__(self,
                 callee: Expr,
                 paren: Token,
                 arguments: list[Expr]):

        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)


class GetExpr(Expr):
    object: Expr
    name: Token

    def __init__(self,
                 object: Expr,
                 name: Token):

        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get_expr(self)


class GroupingExpr(Expr):
    expression: Expr

    def __init__(self,
                 expression: Expr):

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class LiteralExpr(Expr):
    value: object

    def __init__(self,
                 value: object):

        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class LogicalExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __init__(self,
                 left: Expr,
                 operator: Token,
                 right: Expr):

        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)


class SetExpr(Expr):
    object: Expr
    name: Token
    value: Expr

    def __init__(self,
                 object: Expr,
                 name: Token,
                 value: Expr):

        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_set_expr(self)


class SuperExpr(Expr):
    keyword: Token
    method: Token

    def __init__(self,
                 keyword: Token,
                 method: Token):

        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visit_super_expr(self)


class ThisExpr(Expr):
    keyword: Token

    def __init__(self,
                 keyword: Token):

        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visit_this_expr(self)


class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def __init__(self,
                 operator: Token,
                 right: Expr):

        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class VariableExpr(Expr):
    name: Token

    def __init__(self,
                 name: Token):

        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)
