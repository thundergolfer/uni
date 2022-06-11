use std::env;
use std::fs;
use std::io::prelude::*;
use std::net::TcpListener;
use std::net::TcpStream;
use std::thread;
use std::time::Duration;

use hello::ThreadPool;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);
    for stream in listener.incoming() {
        let stream = stream.unwrap();
        // Inefficient, but avoid borrow checker for now when workspace_dir is
        // passed into thread.
        let workspace_dir
            = env::var("BUILD_WORKSPACE_DIRECTORY")
            .expect("Must run web server with `bazel run`.");
        pool.execute(|| {
            handle_connection(workspace_dir, stream);
        });
    }

    println!("Shutting down.");
}

fn handle_connection(workspace_dir: String, mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    stream.read(&mut buffer).unwrap();

    let get = b"GET / HTTP/1.1\r\n";
    let sleep = b"GET /sleep HTTP/1.1\r\n";
    let hello_html_filepath = format!(
        "{}/{}",
        workspace_dir,
        "books/the_rust_programming_language/hello/hello.html"
    );
    let four_o_four_html_filepath = format!(
        "{}/{}",
        workspace_dir,
        "books/the_rust_programming_language/hello/404.html"
    );

    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK", hello_html_filepath)
    } else if buffer.starts_with(sleep) {
        thread::sleep(Duration::from_secs(3));
        ("HTTP/1.1 200 OK", hello_html_filepath)
    } else {
        ("HTTP/1.1 404 NOT FOUND", four_o_four_html_filepath)
    };

    let contents = fs::read_to_string(&filename).unwrap();

    let response = format!(
        "{}\r\nContent-Length: {}\r\n\r\n{}",
        status_line,
        contents.len(),
        contents
    );
    stream.write(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}
