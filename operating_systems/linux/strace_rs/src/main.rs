use std::process;

use tracing::Level;
use tracing_subscriber;

use strace_rs::trace_command;

fn main() {
    let mut args = std::env::args();
    if args.len() < 2 {
        eprintln!(
            "USAGE: {} PROG ARGS",
            args.next().expect("argv[0] always exists")
        );
        process::exit(2);
    } else {
        let _ = args.next().expect("always exists");
    }

    tracing_subscriber::fmt()
        .with_max_level(Level::TRACE)
        .init();

    // We’ll start with the entry point. We check that we were passed a command,
    // and then we fork() to create two processes –
    // one to execute the program to be traced, and
    // the other to trace it.
    let exit_code = unsafe { trace_command(args.into_iter()) };
    process::exit(exit_code);
}
