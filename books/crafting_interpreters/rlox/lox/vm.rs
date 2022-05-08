use super::chunk;
use super::chunk::OpCode;
use super::debug;
use super::value::Value;
use super::value::print_value;

const STACK_MAX: usize = 256;

#[derive(Debug)]
pub struct VM<'a> {
    pub chunk: &'a chunk::Chunk,
    pub ip: usize,
    pub stack: Vec<Value>,
    pub stack_top: usize,
}

impl VM<'_> {
    /// Reset the VM's state, keeping the global variables.
    pub fn reset(&mut self) {
        self.ip = 0;
        self.stack_top = 0;
        self.stack = Vec::new();
    }

    fn push(&mut self, value: Value) {
        self.stack.push(value);
    }

    fn pop(&mut self) -> Value {
        // TODO: Return a Result<Value, RuntimeError>
        self.stack.pop().unwrap()
    }
}

pub enum InterpretResult {
    InterpretOk,
    InterpretCompileError,
    InterpretRuntimeError,
}


pub fn interpret(chunk: &chunk::Chunk) -> InterpretResult {
    let mut vm = VM {
        chunk,
        ip: 0,
        stack: vec![0.0; STACK_MAX],
        stack_top: 0
    };
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
