from oneliner.expr import Expr, ExprVisitor, LiteralExpr, UnaryExpr, \
    BinaryExpr, GroupingExpr, TernaryExpr, AssignExpr, CallExpr, GetExpr, \
    SetExpr, LogicalExpr, ThisExpr, SuperExpr, ListExpr, MapExpr, \
    IndexGetExpr, IndexSetExpr, FunctionExpr, VariableExpr
from oneliner.stmt import Stmt, StmtVisitor, ExpressionStmt, VarStmt, \
    BlockStmt, IfStmt, WhileStmt, FunctionStmt, ReturnStmt, ClassStmt, \
    EmptyStmt
from oneliner.token import Token
from oneliner.utll import stringify


class AstPrinter(ExprVisitor, StmtVisitor):

    def print(self, program: list | Stmt | Expr):
        return print(self.stringify(program))

    def stringify(self, object):
        if isinstance(object, list):
            return "\n".join([
                self.stringify(statement) for statement in object
            ])
        elif isinstance(object, Expr | Stmt):
            return object.accept(self)
        elif isinstance(object, Token):
            return object.lexeme
        elif isinstance(object, tuple):
            return "(" + \
                ":".join([self.stringify(arg) for arg in object]) +\
                ")"
        else:
            return stringify(object, for_debug=True)

    def parenthesize(self, name: str, *args: list):
        text = f"({name}"
        if args:
            text += " " + " ".join([self.stringify(arg) for arg in args])
        return text + ")"

    def visit_expression_stmt(self, stmt: ExpressionStmt):
        return self.parenthesize(";", stmt.expression)

    def visit_binary_expr(self, expr: BinaryExpr):
        return self.parenthesize(f"binary{expr.operator.lexeme}",
                                 expr.left, expr.right)

    def visit_grouping_expr(self, expr: GroupingExpr):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: LiteralExpr):
        return self.parenthesize("literal", expr.value)

    def visit_unary_expr(self, expr: UnaryExpr):
        return self.parenthesize(f"unary{expr.operator.lexeme}",
                                 expr.operand)

    def visit_ternary_expr(self, expr: TernaryExpr):
        return self.parenthesize("ternary",
                                 expr.condition,
                                 expr.then_expr,
                                 expr.else_expr)

    def visit_var_stmt(self, stmt: VarStmt):
        return self.parenthesize("var-decr",
                                 stmt.name,
                                 stmt.initializer)

    def visit_block_stmt(self, stmt: BlockStmt):
        return self.parenthesize("block", stmt.statements)

    def visit_if_stmt(self, stmt: IfStmt):
        return self.parenthesize("if",
                                 stmt.condition,
                                 stmt.then_branch,
                                 stmt.else_branch)

    def visit_while_stmt(self, stmt: WhileStmt):

        return self.parenthesize("while",
                                 stmt.condition,
                                 stmt.body)

    def visit_function_stmt(self, stmt: FunctionStmt):
        return self.parenthesize("function-decr",
                                 stmt.name,
                                 stmt.function)

    def visit_return_stmt(self, stmt: ReturnStmt):
        return self.parenthesize("return", stmt.value)

    def visit_class_stmt(self, stmt: ClassStmt):
        return self.parenthesize("class",
                                 stmt.name,
                                 stmt.superclass,
                                 stmt.methods)

    def visit_empty_stmt(self, stmt: EmptyStmt):
        return self.parenthesize("empty")

    def visit_function_expr(self, expr: FunctionExpr):
        return self.parenthesize("function-body",
                                 expr.params,
                                 expr.body)

    def visit_variable_expr(self, expr: VariableExpr):
        return self.parenthesize("variable", expr.name)

    def visit_assign_expr(self, expr: AssignExpr):
        return self.parenthesize("=", expr.name, expr.value)

    def visit_call_expr(self, expr: CallExpr):
        return self.parenthesize("call",
                                 expr.callee,
                                 expr.arguments)

    def visit_get_expr(self, expr: GetExpr):
        return self.parenthesize(".", expr.object, expr.name)

    def visit_set_expr(self, expr: SetExpr):
        return self.parenthesize(".=",
                                 expr.object,
                                 expr.name,
                                 expr.value)

    def visit_logical_expr(self, expr: LogicalExpr):
        return self.parenthesize(f"logical{expr.operator.lexeme}",
                                 expr.left,
                                 expr.right)

    def visit_this_expr(self, expr: ThisExpr):
        return self.parenthesize("this")

    def visit_super_expr(self, expr: SuperExpr):
        return self.parenthesize("super", expr.method)

    def visit_list_expr(self, expr: ListExpr):
        return self.parenthesize("list", expr.elements)

    def visit_map_expr(self, expr: MapExpr):
        return self.parenthesize("map", expr.elements)

    def visit_index_get_expr(self, expr: IndexGetExpr):
        return self.parenthesize("[]",
                                 expr.object,
                                 expr.index)

    def visit_index_set_expr(self, expr: IndexSetExpr):
        return self.parenthesize("[]=",
                                 expr.object,
                                 expr.index,
                                 expr.value)
