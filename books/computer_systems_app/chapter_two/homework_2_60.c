// 2.60 ♦♦
// Suppose we number the bytes in a w-bit word from 0 (least significant) to w/8-1
// (most significant). Write code for the following C function, which will return an
// unsigned value in which byte `i` of argument `x` has been replaced by byte `b`:
//
//     unsigned replace_byte (unsigned x, int i, unsigned char b);
//
// Here are some examples showing how the function show work:
//
//     replace_byte(0x12345678, 2, 0xAB) --> 0x12AB5678
//     replace_byte(0x12345678, 0, 0xAB) --> 0x123456AB

#include <stdio.h>
// Using `assert` as bare-bones unit testing system.
#include <assert.h>

unsigned replace_byte(unsigned x, int i, unsigned char b) {
    unsigned mask;
    mask = ((1 << 8) - 1) << (i * 8); // get eight 1 bits and shift them into position
    return (x & ~mask) | (b << (i * 8));
}

int main(int argc, char *argv[]) {
    unsigned answer;
    unsigned expected;

    answer = replace_byte(0x12345678, 2, 0xAB);
    expected = 0x12AB5678;
    printf("Value of answer: 0x%08X. Expected: 0x%08X\n", answer, expected);
    assert(answer == expected);

    answer = replace_byte(0x12345678, 0, 0xAB);
    expected = 0x123456AB;
    printf("Value of answer: 0x%08X. Expected: 0x%08X\n", answer, expected);
    assert(answer == expected);
    return 0;
}