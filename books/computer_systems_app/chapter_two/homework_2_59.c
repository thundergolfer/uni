// 2.59 ♦♦
// Write a C expression that will yield a word consisting of the least significant byte of
// `x` and the remaining bytes of `y`. For operands x = 0x89ABCDEF and y = 0x76543210
// this would give 0x765432EF.
#include <stdio.h>
// Using `assert` as bare-bones unit testing system.
#include <assert.h>

int least_byte_of_left_and_rest_of_right(int x, int y) {
    return (y & ~((1 << 8) - 1)) | (x & ((1 << 8) - 1));
}

int main(int argc, char *argv[]) {
    int answer;
    int expected;
    answer = least_byte_of_left_and_rest_of_right(0x89ABCDEF, 0x76543210);
    expected = 0x765432EF;
    printf("Value of answer: 0x%08X. Expected: 0x%08X\n", answer, expected);
    assert(answer == expected);

    answer = least_byte_of_left_and_rest_of_right(0x00000000, 0x00000000);
    expected = 0x00000000;
    printf("Value of answer: 0x%08X. Expected: 0x%08X\n", answer, expected);
    assert(answer == expected);

    answer = least_byte_of_left_and_rest_of_right(0x000000011, 0x22000022);
    expected = 0x22000011;
    printf("Value of answer: 0x%08X. Expected: 0x%08X\n", answer, expected);
    assert(answer == expected);

    answer = least_byte_of_left_and_rest_of_right(0x000000011, 0x22000022);
    expected = 0x22000011;
    printf("Value of answer: 0x%08X. Expected: 0x%08X\n", answer, expected);
    assert(answer == expected);

    return 0;
}