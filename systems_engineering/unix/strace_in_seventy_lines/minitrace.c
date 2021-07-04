// Working through 'Write yourself an strace in 70 lines of code'
// https://blog.nelhage.com/2010/08/write-yourself-an-strace-in-70-lines-of-code/
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

