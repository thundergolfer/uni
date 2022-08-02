/// A Rust translation of the code snippet found in the book's
/// 'Every address you see if virtual' aside, page 126 in version 1.0.0.
use std::alloc::{alloc, dealloc, Layout};

fn main() {
    println!("Location of CODE              : {:p}", main as fn());
    // Rust does not provide manual memory management without `unsafe`.
    // In order to translate the C demo code, which uses malloc(), this
    // `unsafe` block is used to allocate and deallocate a byte of memory
    // on the heap.
    unsafe {
        let layout = Layout::new::<u8>();
        // This ptr must have *some* type, so alloc is coded to always return `*mut u8`.
        // You're supposed to cast the pointer to it's actual pointer type, which is
        // done below.
        let ptr = alloc(layout);
        println!("Location of HEAP              : {:p}", ptr as *const u8);
        *(ptr as *mut u8) = 42;
        assert_eq!(*(ptr as *mut u8), 42);
        // Deallocate to prevent memory leak (even though memory will quickly be reclaimed at process
        // cleanup.
        dealloc(ptr, layout);
    }
    let first = 5;
    let second = 10;
    println!("Location of STACK             : {:p}", &first);
    println!("Location of first stack var   : {:p}", &first);
    println!("Location of seconds stack var : {:p}", &second);
}
