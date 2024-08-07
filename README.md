# OneLiner

[CRAFTING INTERPRETERS](https://craftinginterpreters.com)の[Lox](https://craftinginterpreters.com/the-lox-language.html)のインタプリタ版を、書籍のJava実装を元にPythonで実装して少し手を入れたスクリプト言語です。

## Loxからの差分
1行でのプログラムが書きやすくなるように、以下の変更を加えています。

- 基本型として、リストとマップがある。
  - リストリテラルは `var list = [1,2,3]` のように書き、`list[0]` のようにアクセスする。
  - マップリテラルは `var map = %{"a":1, "b":2, "c":3};` のように書き、`map["a"]` のようにアクセスする。
- print / pは関数である。
```
print(1) # OK
print 1 # NG
```
- ブロックおよびプログラムの最後の式文、return文はセミコロンを省略可能
- 三項演算子 `x ? a : b` を追加
- 文字列リテラルは`"abc"` と `'abc'` の2種類
- メソッド定義の先頭に `method` `mthd` が必要
- 論理演算子を追加(優先度は同じ)
  - `and` `or` `not`
  - `&&` `||` `!`
- 除算を追加
  - `//`: 整数除算
  - `/`: 浮動小数除算
  - `%`: 剰余
- 無名関数を利用可能
  - `λ(x,y){return x+y}`
- 短い予約語が使える
  - `fn`: `fun`
  - `t`: `true`
  - `f`: `false`
    - `v`: `var`
  - `cls`: `class`
  - `mthd`: `method`
  - `λ`: `lambda`, `^`
- ドット記法に続く関数呼び出し `foo.bar(x,y,z)` は、fooがオブジェクトインスタンスの場合はメソッド呼び出しだが、それ以外のプリミティブの場合、 関数呼び出し `bar(foo, x, y, z)` の構文糖衣として扱われる。
- コメントは # から行末まで。ただし#の直後が開き括弧 `{` `[` `(` の場合、それぞれ対応する閉じ括弧 `}` `]` `)` までがコメントとして扱われる


[文法](./grammar.md)