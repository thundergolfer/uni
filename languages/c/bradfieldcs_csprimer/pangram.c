#include <stdbool.h>
#include <nmmintrin.h>
#include <stdio.h>
#include <stdlib.h>

bool ispangram(char *s)
{
  char curr;
  unsigned int bitcount;
  unsigned int bitset = 0;
  for (curr = *s; curr; curr = *s++)
  {
    if (curr >= 'a' && curr <= 'z')
    {
      bitset |= (1 << (curr - 'a'));
    }
    else if (curr >= 'A' && curr <= 'Z')
    {
      bitset |= (1 << (curr - 'A'));
    }
  }
  bitcount = __builtin_popcount(bitset);
  return bitcount == 26;
}

int main()
{
  size_t len;
  ssize_t read;
  char *line = NULL;
  while ((read = getline(&line, &len, stdin)) != -1)
  {
    if (ispangram(line))
      printf("%s", line);
  }

  if (ferror(stdin))
    fprintf(stderr, "Error reading from stdin");

  free(line);
  fprintf(stderr, "ok\n");
}
