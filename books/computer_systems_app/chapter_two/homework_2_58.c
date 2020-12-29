#include <stdio.h>

typedef unsigned char *byte_pointer;

/* Will return 1 when compiled and run on little-endian machine, 0 on big-endian. */
int is_little_endian() {
    int x;
    byte_pointer p;
    // On little-endian the least-significant byte is first.
    // On big-endian the most significant is first.
    // So we can detect little-endian by checking the bytes of an int where *only*
    // the least-significant byte will be non-zero.
    // Integer 1 is such an int.
    x = 1;
    p = (byte_pointer) &x;
    if (p[0]) {
        return 1; // little-endian (01 00 00 00)
    }
    return 0; // big-endian (00 00 00 01)
}

int main(int argc, char *argv[]) {
    int answer;

    answer = is_little_endian();
    if (answer) {
        printf("This program was compiled and run on a little-endian machine.\n");
    } else {
        printf("This program was compiled and run on a BIG-endian machine.\n");
    }
    return 0;
}