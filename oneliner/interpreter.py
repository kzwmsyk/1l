from oneliner.token import TokenType, Token
from oneliner.expr import Expr, LiteralExpr, GroupingExpr, UnaryExpr, \
    BinaryExpr, TernaryExpr
from oneliner.stmt import Stmt, PrintStmt, ExpressionStmt


class RuntimeError(Exception):
    token: Token
    message: str

    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message


class Interpreter:
    # ExprVisitor

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as e:
            print(e)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def stringify(self, value):
        if value is None:
            return "nil"
        else:
            return str(value)

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self.evaluate(stmt.expression)

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
            case TokenType.NOT:
                return not self.is_truthy(operand)
            case _:
                raise RuntimeError(expr.operator, "Unreachable")

    def check_numeric_operand(self, operator: Token, operand):
        if not self.is_numeric(operand):
            raise RuntimeError(operator, "Operand must be number")

    def check_numeric_operands(self, operator: Token, left, right):
        if not (self.is_numeric(left) and self.is_numeric(right)):
            raise RuntimeError(operator, "Operands must be numbers")

    def is_numeric(self, object):
        return isinstance(object, float) or isinstance(object, int)

    def visit_ternary_expr(self, expr: TernaryExpr):
        condition = self.evaluate(expr.condition)
        if self.is_truthy(condition):
            return self.evaluate(expr.then_expr)
        else:
            return self.evaluate(expr.else_expr)

    def visit_binary_expr(self, expr: BinaryExpr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.PLUS:
                if self.is_numeric(left) and self.is_numeric(right):
                    return left + right
                elif isinstance(left, str) and isinstance(right, str):
                    return left + right
                else:
                    raise RuntimeError(
                        expr.operator,
                        "Operands must be two numbers or two strings"
                    )
            case TokenType.MINUS:
                self.check_numeric_operands(expr.operator, left, right)
                return left - right
            case TokenType.STAR:
                self.check_numeric_operands(expr.operator, left, right)
                return left * right
            case TokenType.SLASH:
                self.check_numeric_operands(expr.operator, left, right)
                return left / right
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
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case _:
                raise RuntimeError(expr.operator, "Unreachable")

    def is_equal(self, left, right):
        if left is None and right is None:
            return True
        if left is None:
            return False
        return left == right

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def is_truthy(self, object):
        if object is None:
            return False
        if isinstance(object, bool):
            return object
        return True
