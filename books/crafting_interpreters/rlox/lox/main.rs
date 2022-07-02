use std::env;
use std::io::{self, BufRead, ErrorKind, Write};

use std::path;
use std::process;

mod chunk;
mod compiler;
mod debug;
mod scanner;
mod value;
mod vm;

use crate::vm::InterpretResult;
use chunk::add_constant;
use chunk::build_chunk;
use chunk::write_chunk;
use chunk::Chunk;
use chunk::OpCode;
use debug::disassemble_chunk;
use vm::interpret;

fn repl() {
    print!("> ");
    io::stdout().flush().unwrap();
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        interpret(&line.unwrap());
        print!("> ");
        io::stdout().flush().unwrap();
    }
}

fn run_lox_file(filepath: &str) -> Result<InterpretResult, io::Error> {
    let code = std::fs::read_to_string(filepath)?;
    Ok(interpret(&code))
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() == 1 {
        repl()
    } else if args.len() == 2 {
        match run_lox_file(args[1].as_str()) {
            Ok(InterpretResult::InterpretOk) => process::exit(0),
            Ok(InterpretResult::InterpretCompileError) => process::exit(65),
            Ok(InterpretResult::InterpretRuntimeError) => process::exit(70),
            Err(error) => {
                eprintln!(
                    "{}: can't open file '{}': {}",
                    args[0].as_str(),
                    args[1].as_str(),
                    error.to_string(),
                );
                process::exit(1);
            }
        }
    } else {
        eprintln!("Usage: lox [path]");
        process::exit(64);
    }
}
