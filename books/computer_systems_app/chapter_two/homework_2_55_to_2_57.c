#include <stdio.h>

// Section 2.1  Information Storage
// Code from Page 81 in my 3rd edition of textbook.

typedef unsigned char *byte_pointer;

void show_bytes(byte_pointer start, size_t len) {
    int i;
    for (i = 0; i < len; i++) {
        printf(" %.2x", start[i]);
    }
    printf("\n");
}

void show_int(int x) {
    show_bytes((byte_pointer) &x, sizeof(int));
}

void show_float(float x) {
    show_bytes((byte_pointer) &x, sizeof(float));
}

void show_pointer(void *x) {
    show_bytes((byte_pointer) &x, sizeof(void *));
}

// show_short, show_long, and show_double are part of homework 2.57

void show_short(short x) {
    show_bytes((byte_pointer) &x, sizeof(short));
}

void show_long(long x) {
    show_bytes((byte_pointer) &x, sizeof(long));
}

void show_double(double x) {
    show_bytes((byte_pointer) &x, sizeof(double));
}

void test_show_bytes(int val) {
    int ival = val;
    float fval = (float) ival;
    int *pval = &ival;
    show_int(ival);
    show_float(fval);
    show_pointer(pval);
}

void test_show_bytes_hw_2_57(int val) {
    int ival = val;
    long lval = (long) ival;
    double dval = (double) ival;
    show_short(ival);
    show_long(lval);
    show_double(dval);
}

int main(int argc, char *argv[]) {
    int val = 12345; // Same value as used in textbook (12,345)
    // On my MacBook Pro, this outputs:
    // 39 30 00 00
    // 00 e4 40 46
    // e8 55 8e e8 fe 7f 00 00
    printf("Homework 2.55:\n");
    test_show_bytes(val);

    printf("Homework 2.57:\n");
    test_show_bytes_hw_2_57(val);
    return 0;
}