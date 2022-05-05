mod chunk;
mod debug;
mod value;

use chunk::Chunk;
use chunk::OpCode;
use chunk::add_constant;
use chunk::build_chunk;
use chunk::write_chunk;
use debug::disassemble_chunk;

fn main() {
    println!("Hello, world!");

    let mut c: Chunk = build_chunk();
    println!("{:?}", c);

    let constant = add_constant(&mut c, 1.2);
    write_chunk(&mut c, OpCode::OpConstant { constant });

    write_chunk(&mut c, OpCode::OpReturn);
    write_chunk(&mut c, OpCode::OpReturn);

    disassemble_chunk(&c, "test chunk");

    println!("{:?}", c);
}
