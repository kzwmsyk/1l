
from oneliner.expr import Expr, LiteralExpr, UnaryExpr, BinaryExpr, \
    GroupingExpr


class AstPrinter:

    def print(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: BinaryExpr):
        return self.parenthesize("binary", expr.left, expr.right)

    def visit_grouping_expr(self, expr: GroupingExpr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr):
        return "nil" if expr.value is None else str(expr.value)

    def visit_unary_expr(self, expr: UnaryExpr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *args: list[Expr]):
        text = f"({name}"
        if args:
            text += " " + " ".join([arg.accept(self) for arg in args])
        return text + ")"
