mod chunk;
mod debug;

use chunk::Chunk;
use chunk::OpCode;
use chunk::write_chunk;
use debug::disassemble_chunk;

fn main() {
    println!("Hello, world!");

    let mut c: Chunk = Vec::new();
    println!("{:?}", c);
    write_chunk(&mut c, OpCode::OpReturn);
    write_chunk(&mut c, OpCode::OpReturn);

    disassemble_chunk(&c, "test chunk");

    println!("{:?}", c);
}
