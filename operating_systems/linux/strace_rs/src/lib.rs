#[macro_use]
extern crate num_derive;
#[macro_use]
extern crate bitflags;

use anyhow::{anyhow, bail, Result};
use libc;
use nix::{sys::wait::{WaitPidFlag, WaitStatus}, unistd::Pid};
use std::ffi::CString;
use std::io::Error;
use std::ptr;

use tracing::{debug, error};
pub mod ptrace;

unsafe fn do_child<T>(args: T) -> Result<()>
where
    T: IntoIterator<Item = String>,
{
    let cstrings: Vec<CString> = args
        .into_iter()
        .map(|arg| CString::new(arg.as_str()).expect("CString::new failed"))
        .collect();

    let child_prog = cstrings.get(0).unwrap().clone();
    debug!(?child_prog, "starting child");
    let child_prog = child_prog.into_raw();
    let mut c_pointers: Vec<*const libc::c_char> =
        cstrings.iter().map(|cstr| cstr.as_ptr()).collect();
    // Ensure null termination for C-style argv array
    c_pointers.push(ptr::null());

    let argv: *const *const libc::c_char = c_pointers.as_ptr();

    let mut envp: Vec<*const libc::c_char> = std::env::vars()
        .into_iter()
        .map(|(k, v)| CString::new(format!("{k}={v}")).expect("cannot fail"))
        .map(|cstr| cstr.as_ptr())
        .collect();
    envp.push(ptr::null());
    let envp: *const *const libc::c_char = envp.as_ptr();

    // If a child knows that it wants to be traced, it can make the PTRACE_TRACEME ptrace request, 
    // which starts tracing. In addition, it means that the next signal sent to this process will stop 
    // it and notify the parent (via wait), so that the parent knows to start tracing.
    ptrace::traceme().map_err(|errno| anyhow!("failed TRACEME. errno {}", errno))?; 
    // After doing a TRACEME, we SIGSTOP ourselves so that the parent can continue this
    // child's execution. This assures that the tracer does not miss the early syscalls made by
    // the child.
    let result = libc::raise(libc::SIGSTOP);
    if result == -1 {
        bail!("child failed to SIGSTOP itself. errno {}", Error::last_os_error());
    }

    libc::execve(child_prog, argv, envp);

    // If execution continued to here there was an error.
    let errno: i32 = Error::last_os_error().raw_os_error().unwrap();
    bail!("errno = {}", errno)
}

fn wait_for_status(child: i32) -> Result<bool> {
    loop {
        let status = nix::sys::wait::waitpid(
            Pid::from_raw(child), 
            Some(WaitPidFlag::WUNTRACED)
        )?;
        match status {
            WaitStatus::Exited(_, code) => {
                debug!("{} signalled exited. exit code: {:?}", child, code);
                return Ok(true);  
            },
            WaitStatus::Stopped(_, signal) => {
                debug!("{} signalled stopped: {:?}", child, signal);
                return Ok(false);
            },
            _ => {},
        }
    }
}

fn do_trace(child: i32) -> Result<()> {
    debug!(%child, "starting trace of child");
    let _ = child;
    // Wait until child has sent itself the SIGSTOP above, and is ready to be traced.
    if wait_for_status(child)? {
        bail!("child unexpected exit during trace setup")
    }

    if let Err(errno) = ptrace::setoptions(child, ptrace::Options::SysGood) {
        bail!("failed to ptrace child with PTRACE_O_TRACESYSGOOD. errno={}", errno);
    }

    loop {
        if wait_for_status(child)? {
            break;
        }
        let registers = ptrace::getregs(child)
            .map_err(|errno| anyhow!("ptrace failed errno {}", errno))?;
        let syscall = registers.orig_rax;
        print!("syscall({}) = ", syscall);
        if wait_for_status(child)? {
            break;
        }
        let registers = ptrace::getregs(child)
            .map_err(|errno| anyhow!("ptrace failed errno {}", errno))?;
        let retval = registers.rax;
        println!("{}\n", retval);
    }

    Ok(())
}

pub unsafe fn trace_command<T>(args: T) -> Result<()>
where
    T: IntoIterator<Item = String>,
{
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
