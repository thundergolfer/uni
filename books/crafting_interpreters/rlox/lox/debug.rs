use crate::chunk::Chunk;
use crate::chunk::OpCode;

pub fn disassemble_chunk(chunk: &Chunk, name: &str) {
    println!("== {} ==", name);

    let mut offset = 0;
    while offset < chunk.len() {
        offset = disassemble_instruction(chunk, offset);
    }
}

fn simple_instruction(name: &str, offset: usize) -> usize {
    println!("{}", name);
    return offset + 1;
}

fn disassemble_instruction(chunk: &Chunk, offset: usize) -> usize {
    print!("{:0>4} ", offset);

    let instruction = chunk.get(offset).unwrap();
    return match instruction {
        OpCode::OpReturn => simple_instruction("OP_RETURN", offset),
    }
}
