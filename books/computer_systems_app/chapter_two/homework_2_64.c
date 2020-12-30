// 2.64 ♦
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
// Write code to implement the following function:
//
//     /* Return 1 when any odd bit of x equals 1; 0 otherwise.
//        Assume w=32 */
//     int any_odd_one(unsigned w);
//
// Your function should follow the bit-level integer coding rules (shown above),
// except that you may assume that data type int has w = 32 bits.
#include <stdio.h>

/* Return 1 when any odd bit of x equals 1; 0 otherwise. Assume w=32 */
int any_odd_one(unsigned w) {
    // Is the first bit in a byte the 1st bit or the 0th bit?
    // I'll say that it's the 0th, so the following byte has 1s in all odd positions
    // and 0s elsewhere.
    // 1010 1010
    //
    // Bit-clear any odd bits and check if the value changed.
    return (w & ~0xAAAAAAA) != w;
}

int main(int argc, char *argv[]) {
    int x;

    x = 178956970;
    printf("Are there any 1-valued odd bits in %d?\n", x);
    if (any_odd_one((unsigned) x)) {
        printf("Yes!\n");
    } else {
        printf("No!\n");
    }

    x = 0;
    printf("Are there any 1-valued odd bits in %d?\n", x);
    if (any_odd_one((unsigned) x)) {
        printf("Yes!\n");
    } else {
        printf("No!\n");
    }

    x = 2;
    printf("Are there any 1-valued odd bits in %d?\n", x);
    if (any_odd_one((unsigned) x)) {
        printf("Yes!\n");
    } else {
        printf("No!\n");
    }

    return 0;
}