#! /usr/bin/env python3
import sys
from pathlib import Path
import chevron
import textwrap


def main(args):
    if len(args) != 1:
        print("Usage: generate_ast <output directory>")
        exit(64)
    output_dir = args[0]
    define_ast(output_dir,
               "Expr",
               """
               from oneliner.token import Token
               """,
               {
                   "Assign": [("name", "Token"), ("value", "Expr")],
                   "Binary": [("left", "Expr"),
                              ("operator", "Token"),
                              ("right", "Expr")],
                   "Call": [
                       ("callee", "Expr"),
                       ("paren", "Token"),
                       ("arguments", "list[Expr]")
                   ],
                   "Function": [("params", "list[Token]"),
                                ("body", "list")],  # list[Expr]
                   "Get": [("object", "Expr"), ("name", "Token")],
                   "Grouping": [("expression", "Expr")],
                   "Literal": [("value", "object")],
                   "Logical": [("left", "Expr"), ("operator", "Token"),
                               ("right", "Expr")],
                   "Set": [("object", "Expr"), ("name", "Token"),
                           ("value", "Expr")],
                   "Super": [("keyword", "Token"), ("method", "Token")],
                   "Ternary": [("condition", "Expr"),
                               ("then_expr", "Expr"),
                               ("else_expr", "Expr")],
                   "This": [("keyword", "Token")],
                   "Unary": [("operator", "Token"), ("operand", "Expr")],
                   "Variable": [("name", "Token")],
               })

    define_ast(output_dir,
               "Stmt",
               """
               from oneliner.token import Token
               from oneliner.expr import Expr, VariableExpr, FunctionExpr
               """,
               {
                   "Block": [("statements", "list[Stmt]")],
                   "Expression": [("expression", "Expr")],
                   "Function": [("name", "Token"),
                                ("function", "FunctionExpr")],
                   "Class": [("name", "Token"), ("superclass", "VariableExpr"),
                             ("methods", "list[FunctionStmt]")],
                   "If": [("condition", "Expr"), ("then_branch", "Stmt"),
                          ("else_branch", "Stmt")],
                   "Return": [("keyword", "Token"), ("value", "Expr")],
                   "Var": [("name", "Token"), ("initializer", "Expr")],
                   "While": [("condition", "Expr"), ("body", "Stmt")]
               })


def define_ast(output_dir,
               base_name,
               imports: str,
               types: dict[str, list[tuple[str, str]]]):
    path = Path(output_dir) / (base_name.lower() + ".py")

    type_list = [
        {"subclass_name": key,
         "subclass_name_lc": key.lower(),
         "fields": [
             {"name": name_type[0],
              "type": name_type[1]}
             for name_type in values]}
        for key, values in types.items()
    ]

    for t in type_list:
        fields = t["fields"]
        fields[-1]["is_last"] = True

    with open(path, "w", encoding="utf-8") as writer:
        with open("ast_class.mustache", "r", encoding="utf-8") as template:

            writer.write(chevron.render(template, {
                "base_name": base_name,
                "base_name_lc": base_name.lower(),
                "imports": textwrap.dedent(imports).strip(),
                "types": type_list,

            }))


if __name__ == "__main__":
    main(sys.argv[1:])
