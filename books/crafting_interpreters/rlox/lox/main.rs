mod chunk;

use chunk::Chunk;
use chunk::Opcode;

fn write_chunk(chunk: &mut Chunk, byte: u8) {
    chunk.push(byte);
}

fn main() {
    println!("Hello, world!");

    let mut c: Chunk = Vec::new();
    println!("{:?}", c);
    write_chunk(&mut c, 123);
    write_chunk(&mut c, Opcode::OpReturn as u8);
    println!("{:?}", c);
}
