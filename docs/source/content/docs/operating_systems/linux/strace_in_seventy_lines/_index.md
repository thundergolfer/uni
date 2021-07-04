---
---
## `ministrace`

ministrace is a small strace implementation by **Nelson Elhage**
(@nelhage).

ministrace is a minimal implementation of strace originally about 70
lines of C. It isn't nearly as functional as the real thing, but you
can use it to learn most of what you need to know about the core
interfaces it uses.

ministrace was written for a [blog post][1], which explains in some
detail how it works.

[1]: http://blog.nelhage.com/2010/08/write-yourself-an-strace-in-70-lines-of-code/

### Usage

```ministrace [-n <system call name>|-s <system call int>] <program> <program args>```

Basic ministrace usage just takes a command line:

```ministrace <program> <program args>```

This will run the program provided with the given arguments, and print
out a sequence of all the system calls which made by the program.

#### Build with Bazel

(Only on Linux)

```bazel build //operating_systems/linux/strace_in_seventy_lines:minitrace```

and run:


```bazel run //operating_systems/linux/strace_in_seventy_lines:minitrace -- python -c "print('hello world')"```

