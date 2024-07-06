# Oneliner Grammer
(based on Lox: https://craftinginterpreters.com/appendix-i.html)


```
program       ::= declaration* EOF;
```

## Declarations

```
declaration    ::= classDecl
               | funDecl
               | varDecl
               | statement ;

classDecl      ::= "class" IDENTIFIER ( "<" IDENTIFIER )?
                 "{" function* "}" ;
funDecl        ::= ("fun" | "fn") function ;
varDecl        ::= ("var" | "v") IDENTIFIER ( "=" expression )? ";" ;
```

## Statements
```
statement      ::= exprStmt
               | forStmt
               | ifStmt
               | printStmt
               | returnStmt
               | whileStmt
               | block ;

exprStmt       ::= expression ";" ;
forStmt        ::= "for" "(" ( varDecl | exprStmt | ";" )
                           expression? ";"
                           expression? ")" statement ;
ifStmt         ::= "if" "(" expression ")" statement
                 ( "else" statement )? ;
printStmt      ::= ("print" | "p") expression ";" ;
returnStmt     ::= "return" expression? ";" ;
whileStmt      ::= "while" "(" expression ")" statement ;
block          ::= "{" declaration* "}" ;
```

varDecl, exprStmt, printStmt, retrunStmtのセミコロンは、以下の場合において省略可能で∃。
- プログラム末尾
- ブロックの末尾


## Expressions

```
expression     ::= assignment ;

assignment     ::= ( call "." )? IDENTIFIER "=" assignment
               | ternary ;

ternary        ::= logic_or ("?" expression ":" ternary )?;

logic_or       ::= logic_and ( ("or" | "||") logic_and )* ;
logic_and      ::= equality ( ("and" | "&&") equality )* ;
equality       ::= comparison ( ( "!=" | "==" ) comparison )* ;
comparison     ::= term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           ::= factor ( ( "-" | "+" ) factor )* ;
factor         ::= unary ( ( "/" | "//" | "*" | "%" ) unary )* ;

unary          ::= ( "!" | "not" | "-" ) unary | call ;
call           ::= primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
primary        ::= "true" | "false" | "nil" | "this"
               | NUMBER | STRING | IDENTIFIER | "(" expression ")"
               | "super" "." IDENTIFIER ;
```

## Unity

```
function       ::= IDENTIFIER "(" parameters? ")" block ;
parameters     ::= IDENTIFIER ( "," IDENTIFIER )* ;
arguments      ::= expression ( "," expression )* ;
```

## Lexical

```
NUMBER         ::= DIGIT+ ( "." DIGIT+ )? ;
STRING         ::= "\"" <any char except "\"">* "\""
                | "'" <any char except "'">* "'" ;
IDENTIFIER     ::= ALPHA ( ALPHA | DIGIT )* ;
ALPHA          ::= "a" ... "z" | "A" ... "Z" | "_" ;
DIGIT          ::= "0" ... "9" ;
```