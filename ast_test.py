
from oneliner.expr import Expr, LiteralExpr, UnaryExpr, BinaryExpr, \
    GroupingExpr
from oneliner.token import Token, TokenType
from oneliner.ast_printer import AstPrinter


def main():
    expression = BinaryExpr(
        LiteralExpr(1),
        Token(TokenType.STAR, "*", None, 1),
        LiteralExpr(2)
    )

    print(AstPrinter().print(expression))


if __name__ == "__main__":
    main()
