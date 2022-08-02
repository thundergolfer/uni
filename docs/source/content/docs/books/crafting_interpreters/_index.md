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

I also may complete some bonus implementations.

* [`pylox`](./pylox) (Python Implementation)
* [`rlox`](./rlox) (Rust Implementation)

Textbook code is available at https://github.com/munificent/craftinginterpreters/.

### `jlox` ☕️

#### Usage

I have completed all of part 1 of the textbook! But I have not done any extension exercises,
thus my implementation still fails dozens of the test suite tests.

You can run the `jlox` exe in 'repl' mode: 

```bash
bazel run //books/crafting_interpreters/jlox/lox:Lox
> var foo = 12;
> print foo;
12
```

Or you can pass it a file: 

```bash
bazel run //books/crafting_interpreters/jlox/lox:Lox -- foo.lox
```

#### Testing

**Integration**

I have a script that clones and use's the textbook's test suite. 

```bash
./scripts/run_test.sh
```

----

### `clox` 

I worked on the C implementation of the Lox interpreter straight after finishing `jlox`.
It's a bytecode interpreter using a stack-based virtual machine.

#### Usage 

You can run the `clox` exe in 'repl' mode: 

```bash
bazel run //books/crafting_interpreters/clox/lox
```

Or you can pass it a file: 

```bash
bazel run //books/crafting_interpreters/clox/lox -- foo.lox
```

#### Testing

**Integration**

I have a script that clones and use's the textbook's test suite. 

```bash
TODO(Jonathon): Support clox testing in ./scripts/run_tests.sh
```

----

### `rlox` 🦀

After I've completed that C implementation, `clox`, I'll implement a Lox interpreter in
Rust to both learn Rust better and solidify my learning from the textbook. 

#### Usage

At the moment `rlox` is TODO. 

You can run the `rlox` exe in 'repl' mode: 

```bash
bazel run //books/crafting_interpreters/rlox/lox
```

Or you can pass it a file: 

```bash
TODO
```

#### Testing

**Integration**

I have a script that clones and use's the textbook's test suite. 

```bash
TODO
```
