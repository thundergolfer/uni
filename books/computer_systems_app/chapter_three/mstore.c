// Example code from page 208 in my copy of the textbook.
//
// linux> gcc -Og -S mstore.c

long mult2(long, long);

void multstore(long x, long y, long *dest) {
    long t = mult2(x, y);
    *dest = t;
}