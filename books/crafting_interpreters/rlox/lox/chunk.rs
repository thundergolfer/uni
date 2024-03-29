use super::value;

#[derive(Debug)]
pub struct Chunk {
    pub code: Vec<OpCode>,
    pub constants: value::ValueArray,
    pub lines: Vec<usize>,
}

// TODO(Jonathon): Think about www.reddit.com/r/rust/comments/ui24sa/most_idiomatic_way_to_represent_opcodes/,
// and whether I should refactor this opcode setup.
#[derive(Debug)]
pub enum OpCode {
    OpConstant { constant: usize },
    OpAdd,
    OpSubtract,
    OpMultiply,
    OpDivide,
    OpNegate,
    OpReturn,
}

pub fn build_chunk() -> Chunk {
    Chunk {
        code: Vec::new(),
        constants: value::ValueArray::new(),
        lines: Vec::new(),
    }
}

pub fn write_chunk(chunk: &mut Chunk, code: OpCode, line: usize) {
    chunk.code.push(code);
    chunk.lines.push(line);
}

pub fn add_constant(chunk: &mut Chunk, value: value::Value) -> usize {
    value::write_value_array(&mut chunk.constants, value);
    return chunk.constants.len() - 1;
}
