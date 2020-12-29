// 2.61 ♦♦
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
// Write C expression that evaluate to 1 when the following conditions are true and
// to 0 when they are false. Assume `x` is of type `int`.
//
//  A. Any bit of x equals 1.
//  B. Any bit of x equals 0.
//  C. Any bit in the least significant byte of x equals 1.
//  D. Any bit in the most significant byte of x equals 0.
//
// Your code should follow the bit-level integer coding rules (shown above), with
// the additional restriction that you may not use equality (==) or inequality (!=) tests.
#include <assert.h>
#include <limits.h>
#include <stdio.h>

/*  A. [if] Any bit of x equals 1. [return 1] */
int a_test(int x) {
    // this test amounts to checking if x is 0.
    return !!x;
}

/* B. Any bit of x equals 0. */
int b_test(int x) {
    return !!(x+1); // in two's complement 11111111 (ie. no 0s) is -1.
}

/*  C. Any bit in the least significant byte of x equals 1. */
int c_test(int x) {
    // We can repeat the same test as in a_test after masking
    int mask = (1 << 8) - 1;
    return !!(x & mask);
}

/*  D. Any bit in the most significant byte of x equals 0. */
int d_test(int x) {
    // TODO(Jonathon): Implement
    return 0;
}

int main(int argc, char *argv[]) {
    int i;

    // 0 is the only two's complement integer with no 1 bits.
    assert(a_test(0) == 0);
    assert(b_test(0) == 1);
    for (i = 1; i < INT_MAX; i++) {
        // All two's complement ints > 0 have at least one 1 bit.
        assert(a_test(i) == 1);
        // All two's complement ints > 0 have at least one 0 bit.
        assert(b_test(i) == 1);
    }
    assert(a_test(INT_MAX) == 1);
    assert(b_test(INT_MAX) == 1);
    for (i = INT_MIN; i < -1; i++) {
        // All two's complement ints x ϵ [INT_MIN, -1) have at least one 1 bit.
        assert(a_test(i) == 1);
        // All two's complement ints x ϵ [INT_MIN, -1) have at least one 0 bit.
        assert(b_test(i) == 1);
    }
    // -1 is all 1 bits.
    assert(a_test(-1) == 1);
    // -1 is the only two's complement integer with no 0 bits.
    assert(b_test(-1) == 0);

    printf("Testing C.");

    assert(c_test(0) == 0);
    // NOTE: Not exhaustive testing of C.
    for (i = 1; i <= 255; i++) {
        assert(c_test(i) == 1);
    }
    assert(c_test(256) == 0);

    return 0;
}