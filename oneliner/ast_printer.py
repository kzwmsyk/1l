from oneliner.expr import Expr, ExprVisitor, LiteralExpr, UnaryExpr, \
    BinaryExpr, GroupingExpr, TernaryExpr, AssignExpr, CallExpr, GetExpr, \
    SetExpr, LogicalExpr, ThisExpr, SuperExpr, ListExpr, MapExpr, \
    IndexGetExpr, IndexSetExpr, FunctionExpr, VariableExpr, \
    LiteralExpr, UnaryExpr
from oneliner.stmt import Stmt, StmtVisitor, ExpressionStmt, VarStmt, \
    BlockStmt, IfStmt, WhileStmt, FunctionStmt, ReturnStmt, ClassStmt, \
    EmptyStmt


class AstPrinter(ExprVisitor, StmtVisitor):

    def print(self, program):
        if isinstance(program, list):
            for statement in program:
                self.print(statement)
        else:
            print(program.accept(self))

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        return self.parenthesize(";", stmt.expression)

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

    def visit_var_stmt(self, stmt: VarStmt):
        return ""

    def visit_block_stmt(self, stmt: BlockStmt):
        return ""

    def visit_if_stmt(self, stmt: IfStmt):
        return ""

    def visit_while_stmt(self, stmt: WhileStmt):
        return ""

    def visit_function_stmt(self, stmt: FunctionStmt):
        return ""

    def visit_return_stmt(self, stmt: ReturnStmt):
        return ""

    def visit_class_stmt(self, stmt: ClassStmt):
        return ""

    def visit_empty_stmt(self, stmt: EmptyStmt):
        return ""

    def visit_function_expr(self, expr: FunctionExpr):
        return ""

    def visit_variable_expr(self, expr: VariableExpr):
        return ""

    def visit_assign_expr(self, expr: AssignExpr):
        return ""

    def visit_call_expr(self, expr: CallExpr):
        return ""

    def visit_get_expr(self, expr: GetExpr):
        return ""

    def visit_set_expr(self, expr: SetExpr):
        return ""

    def visit_logical_expr(self, expr: LogicalExpr):
        return ""

    def visit_this_expr(self, expr: ThisExpr):
        return ""

    def visit_super_expr(self, expr: SuperExpr):
        return ""

    def visit_list_expr(self, expr: ListExpr):
        return ""

    def visit_map_expr(self, expr: MapExpr):
        return ""

    def visit_index_get_expr(self, expr: IndexGetExpr):
        return ""

    def visit_index_set_expr(self, expr: IndexSetExpr):
        return ""

    def parenthesize(self, name, *args: list[Expr]):
        text = f"({name}"
        if args:
            text += " " + " ".join([arg.accept(self) for arg in args])
        return text + ")"
