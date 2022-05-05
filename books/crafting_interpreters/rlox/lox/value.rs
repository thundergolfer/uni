use std::vec::Vec;

pub type Value = f64;

// Should I really call this an array, just to match clox?
pub type ValueArray = Vec<Value>;

pub fn write_value_array(array: &mut ValueArray, value: Value) {
    array.push(value);
}

pub fn print_value(value: Value) {
    print!("{}", value);
}
