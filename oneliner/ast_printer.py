
from oneliner.expr import Expr, LiteralExpr, UnaryExpr, BinaryExpr, \
    GroupingExpr, TernaryExpr
from oneliner.stmt import Stmt, PrintStmt, ExpressionStmt


class AstPrinter:
    # ExprVisitor, StmtVisitor

    def print(self, expr_or_stmt):
        return expr_or_stmt.accept(self)

    def print_statements(self, statements: list[Stmt]):
        for statement in statements:
            print(self.print(statement))

    def visit_print_stmt(self, stmt: PrintStmt):
        return self.parenthesize("print", stmt.expression)

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        return self.print(";", stmt.expression)

    def visit_binary_expr(self, expr: BinaryExpr):
        return self.parenthesize("binary", expr.left, expr.right)

    def visit_grouping_expr(self, expr: GroupingExpr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr):
        return "nil" if expr.value is None else str(expr.value)

    def visit_unary_expr(self, expr: UnaryExpr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_ternary_expr(self, expr: TernaryExpr):
        return self.parenthesize("ternary",
                                 expr.condition,
                                 expr.then_expr,
                                 expr.else_expr)

    def parenthesize(self, name, *args: list[Expr]):
        text = f"({name}"
        if args:
            text += " " + " ".join([arg.accept(self) for arg in args])
        return text + ")"
