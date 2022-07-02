use super::chunk;
use super::chunk::OpCode;
use super::debug;
use super::value::print_value;
use super::value::Value;

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
        self.stack_top += 1;
    }

    fn pop(&mut self) -> Value {
        self.stack_top -= 1;
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
        stack_top: 0,
    };
    run(&mut vm)
}

pub fn run(vm: &mut VM) -> InterpretResult {
    loop {
        let op = &vm.chunk.code[vm.ip];
        vm.ip += 1;

        if cfg!(debug_assertions) {
            println!("          ");
            for i in 0..vm.stack_top {
                print!("[ ");
                print_value(vm.stack[i]);
                print!(" ]");
            }
            println!("\n");
        }

        #[cfg(debug_assertions)]
        debug::disassemble_instruction(vm.chunk, vm.ip - 1);

        match op {
            OpCode::OpNegate => {
                let v = vm.pop();
                vm.push(-v);
            }
            OpCode::OpReturn => {
                print_value(vm.pop());
                println!();
                return InterpretResult::InterpretOk;
            }
            OpCode::OpConstant { constant } => {
                let value: Value = vm.chunk.constants[*constant];
                vm.push(value);
                println!();
            }
            OpCode::OpAdd => {
                let a = vm.pop();
                let b = vm.pop();
                vm.push(a + b);
            }
            OpCode::OpSubtract => {
                let a = vm.pop();
                let b = vm.pop();
                vm.push(a - b);
            }
            OpCode::OpMultiply => {
                let a = vm.pop();
                let b = vm.pop();
                vm.push(a * b);
            }
            OpCode::OpDivide => {
                let a = vm.pop();
                let b = vm.pop();
                vm.push(a / b);
            }
        }
    }
}
