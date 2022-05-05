use crate::chunk::Chunk;
use crate::chunk::OpCode;
use crate::value::print_value;

pub fn disassemble_chunk(chunk: &Chunk, name: &str) {
    println!("== {} ==", name);

    let mut offset = 0;
    while offset < chunk.code.len() {
        offset = disassemble_instruction(chunk, offset);
    }
}

fn simple_instruction(name: &str, offset: usize) -> usize {
    println!("{}", name);

    offset + 1
}

fn disassemble_instruction(chunk: &Chunk, offset: usize) -> usize {
    print!("{:0>4} ", offset);

    let instruction = chunk.code.get(offset).unwrap();
    return match instruction {
        OpCode::OpConstant { constant } => constant_instruction("OP_CONSTANT", chunk, *constant, offset),
        OpCode::OpReturn => simple_instruction("OP_RETURN", offset),
    }
}

fn constant_instruction(
    name: &str,
    chunk: &Chunk,
    constant: usize,
    offset: usize) -> usize {
    print!("{:16} {} '", name, constant);
    print_value(*chunk.constants.get(constant).unwrap());
    println!("'");

    // Don't need to handle the variable length of opcodes in rlox,
    // so this offset tracking mechanism isn't very useful.
    offset + 1
}
