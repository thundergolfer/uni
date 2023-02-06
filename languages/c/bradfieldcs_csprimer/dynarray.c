#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

void *reallocate(void *pointer, size_t newSize)
{
  if (newSize == 0)
  {
    free(pointer);
    return NULL;
  }
  void *result = realloc(pointer, newSize);
  if (result == NULL)
    exit(1);
  return result;
}

#define STARTING_CAPACITY 8

typedef struct DA
{
  size_t capacity;
  size_t len;
  void **values;
} DA;

DA *DA_new(void)
{
  struct DA *da = malloc(sizeof(struct DA));
  da->capacity = STARTING_CAPACITY;
  da->len = 0;
  da->values = (void *)malloc(sizeof(void *) * STARTING_CAPACITY);
  return da;
}

int DA_size(DA *da)
{
  // TODO return the number of items in the dynamic array
  return da->len;
}

void DA_push(DA *da, void *x)
{
  if (da->capacity == da->len)
  {
    da->capacity <<= 1;
    da->values = reallocate(da->values, da->capacity * sizeof(void *));
  }
  da->values[da->len++] = x;
}

void *DA_pop(DA *da)
{
  if (da->len == 0)
  {
    return NULL;
  }
  void *popped = da->values[da->len - 1];
  da->len--; // TODO: do -- inline?
  return popped;
}

void DA_set(DA *da, void *x, int i)
{
  // TODO set at a given index, if possible
  if (da->len <= i)
    return; // index out of bounds
  da->values[i] = x;
}

void *DA_get(DA *da, int i)
{
  if (da->len <= i)
    return NULL; // index out of bounds
  return da->values[i];
}

void DA_free(DA *da)
{
  reallocate(da->values, 0);
  free(da);
}

int main()
{
  DA *da = DA_new();

  assert(DA_size(da) == 0);

  // basic push and pop test
  int x = 5;
  float y = 12.4;
  DA_push(da, &x);
  DA_push(da, &y);
  assert(DA_size(da) == 2);

  assert(DA_pop(da) == &y);
  assert(DA_size(da) == 1);

  assert(DA_pop(da) == &x);
  assert(DA_size(da) == 0);
  assert(DA_pop(da) == NULL);

  // basic set/get test
  DA_push(da, &x);
  DA_set(da, &y, 0);
  assert(DA_get(da, 0) == &y);
  DA_pop(da);
  assert(DA_size(da) == 0);

  // expansion test
  DA *da2 = DA_new(); // use another DA to show it doesn't get overriden
  DA_push(da2, &x);
  int i, n = 20 * STARTING_CAPACITY, arr[n];
  for (i = 0; i < n; i++)
  {
    arr[i] = i;
    DA_push(da, &arr[i]);
  }

  assert(DA_size(da) == n);
  for (i = 0; i < n; i++)
  {
    assert(DA_get(da, i) == &arr[i]);
  }
  for (; n; n--)
    DA_pop(da);
  assert(DA_size(da) == 0);
  assert(DA_pop(da2) == &x); // this will fail if da doesn't expand

  DA_free(da);
  DA_free(da2);
  printf("OK\n");
}
