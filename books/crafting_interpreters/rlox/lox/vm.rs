use super::chunk;
use super::chunk::OpCode;
use super::debug;
use super::value::Value;
use super::value::print_value;

#[derive(Debug)]
pub struct VM<'a> {
    pub chunk: &'a chunk::Chunk,
    pub ip: usize,
}

pub enum InterpretResult {
    InterpretOk,
    InterpretCompileError,
    InterpretRuntimeError,
}

pub fn interpret(chunk: &chunk::Chunk) -> InterpretResult {
    let mut vm = VM { chunk, ip: 0 };
    run(&mut vm)
}

pub fn run(vm: &mut VM) -> InterpretResult {
    loop {
        let op = &vm.chunk.code[vm.ip];
        vm.ip += 1;

        #[cfg(debug_assertions)]
        debug::disassemble_instruction(vm.chunk, vm.ip-1);

        match op {
            OpCode::OpReturn => return InterpretResult::InterpretOk,
            OpCode::OpConstant { constant } => {
                let value: Value = vm.chunk.constants[*constant];
                print_value(value);
                println!();
            },
        }
    }
}
