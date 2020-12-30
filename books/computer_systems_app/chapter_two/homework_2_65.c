// 2.65 ♦♦♦♦ (👩‍🔬 Lab Assignment, requiring up to 10 hours.)
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
//     /* Return 1 when x contains an odd number of 1s; 0 otherwise.
//     int odd_ones(unsigned x);
//
// You function should follow the bit-level integer coding rules (shown above),
// except that you may assume that data type`int` has `w = 32` bits.
// Your code should contain a total of at most 12 arithmetic, bitwise, and logical operations.

int odd_ones(unsigned x) {
    return 0; // TODO(Jonathon): Implement this.
}

int main(int argc, char *argv[]) {
    return 0;
}