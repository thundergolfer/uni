---
---
## [_Crafting Interpreters_](https://craftinginterpreters.com/)

> by Robert Nystrom ([@munificentbob](https://twitter.com/intent/user?screen_name=munificentbob))

I worked on the 1st Print Edition. Unlike a lot of the other books worked on in this monorepo,
the code doesn't follow a chapter-by-chapter structure, as it's not appropriate in this case.

This book covers off two implementations of a programming language called **Lox**, and each gets its
own folder.

* [`jlox`](./jlox) (Java Implementation)
* [`clox`](./clox) (C Implementation)

Textbook code is available at https://github.com/munificent/craftinginterpreters/.

### `jlox` 

#### Usage

At the moment all my JLox implementation can do is scan/lex Lox and print out the tokens. 

You can run the `jlox` exe in 'repl' mode: 

```bash
bazel run //books/crafting_interpreters/jlox/lox:Lox
> var foo = 12;
VAR var null
IDENTIFIER foo null
EQUAL = null
NUMBER 123 123.0
SEMICOLON ; null
EOF  null
```

Or you can pass it a file: 

```bash
bazel run //books/crafting_interpreters/jlox/lox:Lox -- foo.lox
```
