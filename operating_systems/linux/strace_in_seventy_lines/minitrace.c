// Working through 'Write yourself an strace in 70 lines of code'
// https://blog.nelhage.com/2010/08/write-yourself-an-strace-in-70-lines-of-code/
//
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/wait.h>
#include <sys/types.h>
// The <unistd.h> header defines miscellaneous symbolic constants and types, and declares miscellaneous functions. The contents of this header are shown below.
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

int do_child(int argc, char **argv) {
    char *args [argc+1];
    memcpy(args, argv, argc * sizeof(char*));
    args[argc] = NULL;
    // The child starts with some trivial marshalling of arguments, since execvp wants a NULL-terminated argument array.
    ptrace(PTRACE_TRACEME);
    kill(getpid(), SIGSTOP);
    // Next, we just execute the provided argument list, but first, we need to start the tracing process, so 
    // that the parent can start tracing the newly-executed program from the very start.
    // If a child knows that it wants to be traced, it can make the PTRACE_TRACEME ptrace request, 
    // which starts tracing. In addition, it means that the next signal sent to this process will stop 
    // it and notify the parent (via wait), so that the parent knows to start tracing. 
    // So, after doing a TRACEME, we SIGSTOP ourselves, so that the parent can continue our execution with the exec call.
    return execvp(args[0], args);
}

int wait_for_syscall(pid_t child);

int do_trace(pid_t child) {
    int status;
    int syscall;
    int retval;
    // In the parent, meanwhile, we prototype a function we’ll need later, and start tracing. 
    // We immediately waitpid on the child, which will return once the child has sent itself the SIGSTOP above, and is ready to be traced.
    waitpid(child, &status, 0);

    ptrace(PTRACE_SETOPTIONS, child, 0, PTRACE_O_TRACESYSGOOD);

    while(1) {
        // Now we enter the tracing loop. wait_for_syscall, defined below, will run the 
        // child until either entry to or exit from a system call. If it returns non-zero, the child has exited and we end the loop.
        if (wait_for_syscall(child) != 0) break;
        syscall = ptrace(PTRACE_PEEKUSER, child, sizeof(long)*ORIG_RAX);  // ORIG_EAX comes from sys/reg.h IF 32-bit. Otherwise ORIG_RAX is provided. Original blog used ORIG_EAX, think because it was using 32-bit i386.
        fprintf(stderr, "syscall(%d) = ", syscall);
        if (wait_for_syscall(child) != 0) break;
        retval = ptrace(PTRACE_PEEKUSER, child, sizeof(long)*RAX);  // EAX on 32-bit i386. RAX on 64-bit.
        fprintf(stderr, "%d\n", retval);
    }

    return 0;
}

int wait_for_syscall(pid_t child) {
    int status;
    while (1) {
        ptrace(PTRACE_SYSCALL, child, 0, 0);
        waitpid(child, &status, 0);

        if (WIFSTOPPED(status) && WSTOPSIG(status) & 0x80) {
            return 0;
        }

        if (WIFEXITED(status)) {
            return 1;
        }
    }
}

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s PROG ARGS\n", argv[0]);
        exit(1);
    }

    // We’ll start with the entry point. We check that we were passed a command, and 
    // then we fork() to create two processes – one to execute the program to be traced, and the other to trace it.
    pid_t child = fork();
    if (child == 0) {
        return do_child(argc-1  , argv+1);
    } else {
        return do_trace(child);
    }
}
