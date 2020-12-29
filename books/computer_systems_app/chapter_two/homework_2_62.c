// 2.62 ♦♦♦
//
// ______________________________________________________________________________________________________
// BIT-LEVEL INTEGER CODING RULES
// In several of the following problems, we will artificially restrict what programming
// constructs you can use to help you gain a better understanding of the bit-level,
// logic, and arithmetic operations of C. In answering these problems, your code
// must follow these rules:
//
// • Assumptions
//      ▪ Integers are represented in two's complement form.
//      ▪ Right shifts of signed data are performed arithmetically.
//      ▪ Data type `int` is `w` bits long. For some of the problems, you will be given a
//        specific value for `w`, but otherwise you code should work as long as `w` is a multiple of 8.
//        You can use the expression `sizeof(int)<<3` to compute `w`.
// • Forbidden
//      ▪ Conditionals (`if` or `?:`), loops, switch statements, function calls, and macro invocations.
//      ▪ Division, modulus, and multiplication.
//      ▪ Relative comparison operators (<, >, <=, and >=)
// • Allowed operations
//      ▪ All bit-level and logic operations.
//      ▪ Left and right shifts, but only with shift amounts between 0 and w-1.
//      ▪ Addition and subtraction.
//      ▪ Equality (==) and inequality (!=) tests. (Some of the problems do not allow these.)
//      ▪ Integer constants INT_MIN and INT_MAX.
//      ▪ Casting between data types `int` and `unsigned`, either explicitly or implicitly.
// ______________________________________________________________________________________________________
//
// Write a function `int_shifts_are_arithmetic()` that yields 1 when run on a
// machine that uses arithmetic shifts for data type int and yields 0 otherwise.
// Your code should work on a machine with any word size. Test your code on several machines.
#include <assert.h>
#include <limits.h>
#include <stdio.h>
