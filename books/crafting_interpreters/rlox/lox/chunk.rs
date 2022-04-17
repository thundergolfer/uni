pub type Chunk = Vec<OpCode>;

#[derive(Debug)]
pub enum OpCode {
    OpReturn,
}

pub fn write_chunk(chunk: &mut Chunk, code: OpCode) {
    chunk.push(code);
}
