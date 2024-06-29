# 1l - oneline programming language


## commandline option

```
オプション	説明
-a	オートスプリットモード。-n または -p と組み合わせた場合、入力をスペースで自動的に区切って、予約変数 @F に代入します。
-d	perl をデバッグモードで起動します。
-Dnumber	デバッグフラグ。このフラグを使用するには、perl がデバッグモードでコンパイルされている必要があります。
-e script	script を perl のスクリプトとして実行します。例えば、「perl -e "print 5 * 3"」 は 5 * 3 の結果 15 を表示します。
-iext	perl -p -i.bak -e "s/\r\n/\n/" file1.txt とすると、file1.txt ファイルに対して s/\r\n/\n/ の操作（Windows 形式の改行から UNIX 形式の改行への変換）を行い、file1.txt を更新します。また、file1.txt のバックアップを file1.txt.bak として残します。
-n	スクリプトを while (<>) { ... } で囲んで実行します。
-p	スクリプトを while (<>) { ... } continue { print; } で囲んで実行します。
-v	perl のバージョン情報を表示します。
-V	perl の詳しいバージョン情報を表示します。
-w	未使用変数、未初期化変数の参照などの警告を表示します。
-xdir	#! で始まって perl という文字を含む行までをコメントとして読み飛ばします。ディレクトリ dir を指定した場合は、そのディレクトリに移動してから処理を行います。
```

## Supports

### literals
- boolean: true, false
- integer: 1, 2, -1, ...
- float: 1.1, -1.1, ...
- string: "hello", qq(hello), 'hello', q(hello)
- array: [1,2,3]
- object(hash, dict): {key1: value1, key2: value2}
- regex: /.+/

### operators
- + - * / %
- ()
- == != < > <= >= === !==
- && || !
- cond ? iftrue : iffalse

### control flow

#### 復文
statement := (statement; statement)
statement := (statement| statement)
#### sequential1

```
statement; statement
```
#### sequential2
前のstatementの結果を$_に代入して後のstatementを実行
```
statement1|statement2|statement3
```

### conditional
```
if cond: statement elif cond: statement else: statement


```


### for loop
```
for $a in $loop {statements}; statements
for $a in $loop {statements}| statements
```

```

```

### 