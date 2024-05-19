
#[macro_use]
extern crate num_derive;
#[macro_use]
extern crate bitflags;

use libc;
use std::ffi::CString;
use std::io::Error;
use std::ptr;

use tracing::{debug, error};
pub mod ptrace;

unsafe fn do_child<T>(args: T) -> i32
where T: IntoIterator<Item = String> {
    let cstrings: Vec<CString> = args.into_iter()
        .map(|arg| CString::new(arg.as_str()).expect("CString::new failed"))
        .collect();

    let child_prog = cstrings.get(0).unwrap().clone();
    debug!(?child_prog, "starting child");
    let child_prog = child_prog.into_raw();
    let mut c_pointers: Vec<*const libc::c_char> = cstrings
        .iter()
        .map(|cstr| cstr.as_ptr())
        .collect();
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

    // If execution continued to here there was an error.
    let errno: i32 = Error::last_os_error().raw_os_error().unwrap();
    error!("errno = {}", errno);
    errno
}

fn do_trace(child: i32) -> i32 {
    debug!(%child, "starting trace of child");
    let _ = child;
    std::thread::sleep(std::time::Duration::from_secs(2));
    0
}

pub unsafe fn trace_command<T>(args: T) -> i32 
where T: IntoIterator<Item = String> {
    unsafe {
        let child = libc::fork();
        debug!(?child, "after fork");
        if child == 0 {
            do_child(args)
        } else {
            do_trace(child)
        }
    }
}
