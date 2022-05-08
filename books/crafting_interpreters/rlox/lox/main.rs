mod chunk;
mod debug;
mod value;
mod vm;

use chunk::Chunk;
use chunk::OpCode;
use chunk::add_constant;
use chunk::build_chunk;
use chunk::write_chunk;
use debug::disassemble_chunk;
use vm::interpret;

fn main() {
    let mut c: Chunk = build_chunk();

    let constant = add_constant(&mut c, 1.2);
    write_chunk(&mut c, OpCode::OpConstant { constant }, 123);

    write_chunk(&mut c, OpCode::OpReturn, 123);
    write_chunk(&mut c, OpCode::OpReturn, 123);

    disassemble_chunk(&c, "test chunk");
    interpret(&c);
    println!("{:?}", c);
}
