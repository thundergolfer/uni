use libc;
use std::ffi::CString;
use std::io::Error;
use std::process;
use std::ptr;

use tracing::{debug, info, warn, error, Level};
use tracing_subscriber;

unsafe fn do_child<T>(args: T) -> i32
where T: IntoIterator<Item = String> {
    let cstrings: Vec<CString> = args.into_iter()
        .map(|arg| CString::new(arg.as_str()).expect("CString::new failed"))
        .collect();

    let child_prog = cstrings.get(0).unwrap().clone();
    debug!(?child_prog, "starting child");
    let child_prog = child_prog.into_raw();

    // Step 3: Store pointers to these CStrings in a Vec<*const c_char>
    let mut c_pointers: Vec<*const libc::c_char> = cstrings
        .iter()
        .map(|cstr| cstr.as_ptr())
        .collect();

    // Step 4: Convert this Vec<*const c_char> to a raw pointer
    // Ensure null termination for C-style argv array
    c_pointers.push(ptr::null());

    let argv: *const *const libc::c_char = c_pointers.as_ptr();

    let mut envp: Vec<*const libc::c_char> = std::env::vars()
            .into_iter()
            .map(|(k,v)| CString::new(format!("{k}={v}")).expect("cannot fail"))
            .map(|cstr| cstr.as_ptr())
            .collect();
    envp.push(ptr::null());
    let envp: *const *const libc::c_char = envp.as_ptr();
    libc::execve(child_prog, argv, envp);

    // If execution continued there was an error.
    let errno: i32 = Error::last_os_error().raw_os_error().unwrap();
    error!("errno = {}", errno);
    1
}

fn do_trace(child: i32) -> i32 {
    debug!(%child, "starting trace of child");
    let _ = child;
    std::thread::sleep(std::time::Duration::from_secs(2));
    0
}

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
    
    let argv = args.into_iter();

    tracing_subscriber::fmt()
        .with_max_level(Level::TRACE)
        .init();

    info!("This is an info message.");
    warn!("This is a warning message.");
    error!("This is an error message.");
    debug!("This is a debug message.");

    // We’ll start with the entry point. We check that we were passed a command,
    // and then we fork() to create two processes –
    // one to execute the program to be traced, and
    // the other to trace it.
    let exit_code = unsafe {
        let child = libc::fork();
        debug!(?child, "after fork");
        if child == 0 {
            do_child(argv)
        } else {
            do_trace(child)
        }
    };
    process::exit(exit_code);
}
