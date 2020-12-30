// 2.63 ♦♦♦
//
// Fill in code for the following C functions. Function `sr1` performs a logical right
// shift using an arithmetic right shift (given by value `xsra`), followed by other operations
// not including right shifts or division. Function `sra` performs an arithmetic
// right shift using a logical right (given by value `xsr1`), followed by other
// operations not including right shifts or divisions. You may use the computation
// `8*sizeof(int)` to determine `w`, the number of bits in datatype `int`. The shift
// amount `k` can range from 0 to w-1.
#include <stdio.h>

unsigned sr1(unsigned x, int k) {
    /* Perform shift arithmetically */
    unsigned xsra = (int) x >> k;
    return 0; // TODO(Jonathon): Actually implement.
}

int sra(int x, int k) {
    /* Perform shift logically */
    int xsr1 = (unsigned) x >> k;
    return 0; // TODO(Jonathon): Actually implement.
}

int main(int argc, char *argv[]) {
    return 0;
}