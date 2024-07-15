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

classDecl      ::= ("class" | "cls") IDENTIFIER ( "<" IDENTIFIER )?
                 "{" ("method" | "mthd") function* "}" ;
funDecl        ::= ("fun" | "fn") function ;
varDecl        ::= ("var" | "v") IDENTIFIER ( "=" expression )? ";" ;
```

## Statements
```
statement      ::= emptyStmt
               | exprStmt
               | forStmt
               | ifStmt
               | returnStmt
               | whileStmt
               | block ;

emptyStmt      ::= ";" ;
exprStmt       ::= expression ";" ;
forStmt        ::= "for" "(" ( varDecl | exprStmt | ";" )
                           expression? ";"
                           expression? ")" statement ;
ifStmt         ::= "if" "(" expression ")" statement
                 ( "else" statement )? ;
returnStmt     ::= "return" expression? ";" ;
whileStmt      ::= "while" "(" expression ")" statement ;
block          ::= "{" declaration* "}" ;
```

semicolons of varDecl, exprStmt, printStmt, retrunStmt are omittable at the end of program or block.


## Expressions

```
expression     ::= assignment ;

assignment     ::= ( call "." )? IDENTIFIER (index)? "=" assignment
               | ternary ;

ternary        ::= logic_or ("?" expression ":" ternary )?;

logic_or       ::= logic_and ( ("or" | "||") logic_and )* ;
logic_and      ::= equality ( ("and" | "&&") equality )* ;
equality       ::= comparison ( ( "!=" | "==" ) comparison )* ;
comparison     ::= term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           ::= factor ( ( "-" | "+" ) factor )* ;
factor         ::= unary ( ( "/" | "//" | "*" | "%" ) unary )* ;

unary          ::= ( "!" | "not" | "-" ) unary | call ;
call           ::= primary ( "(" arguments? ")" | "." IDENTIFIER | index)* ;
primary        ::= "true" | "false" | "nil" | "this"
                | list | map
                | lambda
                | NUMBER | STRING | IDENTIFIER | "(" expression ")"
                | "super" "." IDENTIFIER ;
index          ::= "[" expression "]" ;
list           ::= "[" elements? "]" ;
map            ::= "%{" pairs? "}" ;
elements      ::= expression ( "," expression )* ;
pairs          ::= expression ":" expression ( "," expression ":" expression )* ;
```

## Unity

```
function       ::= IDENTIFIER function_body ;
function_body  ::= "(" parameters? ")" block
parameters     ::= IDENTIFIER ( "," IDENTIFIER )* ;
arguments      ::= expression ( "," expression )* ;
lambda         ::= ("λ" | "^" | "lambda") function_body ;
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