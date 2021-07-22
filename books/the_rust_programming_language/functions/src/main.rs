fn five() -> i32 {
    5
}

fn plus_one(x: i32) -> i32 {
    x + 1
}

fn main() {
    let _x = five();
    let x = plus_one(5);

    println!("The value of x is : {}", x);

    another_function(5, 10);
}

fn another_function(x: i32, y: i32) {
    println!("The value of x is: {}", x);
    println!("The value of y is: {}", y);
}
