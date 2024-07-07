# OneLiner

[CRAFTING INTERPRETERS](https://craftinginterpreters.com)の[Lox](https://craftinginterpreters.com/the-lox-language.html)のインタプリタ版を、書籍のJava実装を元にPythonで実装して少し手を入れたスクリプト言語です。

1行でのプログラムが書きやすくなるように、以下の変更を加えています。

- ブロックおよびプログラムの最後の式文、print文、return文はセミコロンを省略可能
- 三項演算子 `x ? a : b` を追加
- 文字列リテラルは`"abc"` と `'abc'` の2種類
- 論理演算子を追加(優先度は同じ)
  - `and` `or` `not`
  - `&&` `||` `!`
- 除算を追加
  - `//`: 整数除算
  - `/`: 浮動小数除算
  - `%`: 剰余
- 短い予約語が使える
  - `fn`: `fun`
  - `t`: `true`
  - `f`: `false`
  - `p`: `print`
  - `v`: `var`
- メソッド定義の先頭に `method` `m` が必要

[文法](./grammar.md)