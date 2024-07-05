from oneliner.token import Token, TokenType
from oneliner.expr import Expr, BinaryExpr, UnaryExpr, LiteralExpr, \
    GroupingExpr, TernaryExpr, VariableExpr, AssignExpr, LogicalExpr, \
    CallExpr
from oneliner.stmt import Stmt, PrintStmt, ExpressionStmt, VarStmt, \
    BlockStmt, IfStmt, WhileStmt, FunctionStmt, ReturnStmt
from oneliner.error import ParseError, ErrorReporter


class Parser:

    def __init__(self, tokens: list[Token], error_reporter: ErrorReporter):
        self.current: int = 0
        self.tokens = tokens
        self.error_reporter = error_reporter

    def parse(self) -> list[Stmt]:
        try:
            statements: list[Stmt] = []
            while not self.is_at_end():
                statements.append(self.declaration())
            return statements
        except ParseError:
            return None

    #
    # statements
    #

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def var_declaration(self):

        name: Token = self.consume(
            TokenType.IDENTIFIER, "Expect variable name.")
        initializer: Expr = None

        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON,
                     "Expect ';' after variable declaration.")
        return VarStmt(name, initializer)

    def function(self, kind: str) -> FunctionStmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect " + kind + " name.")

        self.consume(TokenType.LEFT_PAREN,
                     "Expect '(' after " + kind + " name.")

        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) > 255:
                    self.error_reporter.token_error(
                        self.peek(),
                        "Can't have more than 255 parameters."
                    )
                parameters.append(self.consume(
                    TokenType.IDENTIFIER, "Expect parameter name."))

                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.consume(TokenType.LEFT_BRACE,
                     "Expect '{' before " + kind + " body.")
        body: list[Stmt] = self.block_statement()
        return FunctionStmt(name, parameters, body)

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()

        if self.match(TokenType.RETURN):
            return self.return_statement()

        if self.match(TokenType.LEFT_BRACE):
            return BlockStmt(self.block_statement())

        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.WHILE):
            return self.while_statement()

        if self.match(TokenType.FOR):
            return self.for_statement()

        # TODO: ほかのぶん
        return self.expression_statement()

    def print_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return PrintStmt(expr)

    def return_statement(self) -> Stmt:
        keyword = self.previous()
        value = None
        if (not self.check(TokenType.SEMICOLON)):
            value = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStmt(keyword, value)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStmt(expr)

    def block_statement(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def if_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None

        # elseは最も近いifとくっつく
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return IfStmt(condition, then_branch, else_branch)

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        body = self.statement()
        return WhileStmt(condition, body)

    # for(initializer; condition: ) {}
    def for_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        # initializer
        initializer: Stmt = None
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition: Expr = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition")

        increment: Expr = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clause.")

        body = self.statement()

        if increment is not None:
            body = BlockStmt([
                body,
                ExpressionStmt(increment)
            ])

        if condition is None:
            condition = LiteralExpr(True)
        body = WhileStmt(condition, body)

        if initializer is not None:
            body = BlockStmt([initializer, body])

        return body

    #
    # expressions
    #

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        expr = self.ternary()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, VariableExpr):
                name: Token = expr.name
                return AssignExpr(name, value)

            self.error(equals, "Invalid assignment target.")
        return expr

    def ternary(self) -> Expr:
        expr = self.logical_or()
        if self.match(TokenType.QUESTION):
            then_expr = self.expression()
            self.consume(TokenType.COLON, "Expect ':' after '?' expr ")
            else_expr = self.ternary()
            return TernaryExpr(expr, then_expr, else_expr)
        return expr

    def logical_or(self) -> Expr:
        expr = self.logical_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logical_and()
            expr = LogicalExpr(expr, operator, right)
        return expr

    def logical_and(self) -> Expr:
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = LogicalExpr(expr, operator, right)
        return expr

    def equality(self) -> Expr:
        expr = self.comparison()
        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def comparison(self) -> Expr:
        expr = self.term()

        while (self.match(TokenType.GREATER, TokenType.GREATER_EQUAL,
                          TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while (self.match(TokenType.MINUS, TokenType.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while (self.match(TokenType.SLASH, TokenType.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)
        return self.call()

    def call(self) -> Expr:
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            else:
                break
        return expr

    def finish_call(self, callee: Expr) -> Expr:
        arguments: list[Expr] = []

        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.error_reporter.token_error(
                        self.peek(),
                        "Can't have more than 255 ar====guments."
                    )
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break

        paren = self.consume(TokenType.RIGHT_PAREN,
                             "Expect ')' after arguments.")
        return CallExpr(callee, paren, arguments)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return LiteralExpr(False)
        if self.match(TokenType.TRUE):
            return LiteralExpr(True)
        if self.match(TokenType.NIL):
            return LiteralExpr(None)

        if self.match(TokenType.INT, TokenType.FLOAT, TokenType.STRING):
            return LiteralExpr(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            return VariableExpr(self.previous())

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        raise self.error(self.peek(), "Expect expression")

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str) -> ParseError:
        self.error_reporter.token_error(token, message)
        return ParseError(f"[line {token.line}] Error: {message}")

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            match self.peek().type:
                case TokenType.CLASS | TokenType.FUN | TokenType.VAR |\
                        TokenType.FOR | TokenType.IF | TokenType.WHILE |\
                        TokenType.PRINT | TokenType.RETURN:
                    return
            self.advance()
