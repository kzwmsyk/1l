from oneliner.token import Token


class Expr:
    # Visitor Interface
    # class Visitor<R>:
    #     R visit_foo_stmt(Foo stmt)
    #     R visit_bar_expr(Bar expr)

    def accept(visitor):
        pass


class AssignExpr(Expr):
    def __init__(self,
                 name: Token,
                 value: Expr):

        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class BinaryExpr(Expr):
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
    def __init__(self,
                 object: Expr,
                 name: Token):

        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visit_get_expr(self)


class GroupingExpr(Expr):
    def __init__(self,
                 expression: Expr):

        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class LiteralExpr(Expr):
    def __init__(self,
                 value: object):

        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class LogicalExpr(Expr):
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
    def __init__(self,
                 keyword: Token,
                 method: Token):

        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visit_super_expr(self)


class ThisExpr(Expr):
    def __init__(self,
                 keyword: Token):

        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visit_this_expr(self)


class UnaryExpr(Expr):
    def __init__(self,
                 operator: Token,
                 operand: Expr):

        self.operator = operator
        self.operand = operand

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class VariableExpr(Expr):
    def __init__(self,
                 name: Token):

        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)
