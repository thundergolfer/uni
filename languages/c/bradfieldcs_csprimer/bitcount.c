#include <assert.h>
#include <nmmintrin.h>
#include <stdio.h>

int bitcount(unsigned int value)
{
    int count;
    for (count = 0; value > 0; value &= (value - 1))
    {
        count++;
    }
    return count;
}

int bitcount_builtin(value)
{
    return __builtin_popcount(value);
}

int main()
{
    assert(bitcount(0) == 0);
    assert(bitcount(1) == 1);
    assert(bitcount(3) == 2);
    assert(bitcount(8) == 1);
    assert(bitcount_builtin(8) == 1);
    // harder case:
    assert(bitcount(0xffffffff) == 32);
    assert(bitcount_builtin(0xffffffff) == 32);
    printf("OK\n");
}
