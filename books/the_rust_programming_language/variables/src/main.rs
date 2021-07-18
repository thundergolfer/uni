fn main() {
    let mut x = 5;
    println!("The value of x is: {}", x);
    x = 6; // Doesn't compile.
    println!("The value of x is: {}", x);

    const MAX_POINTS: u32 = 100_000;

    let tup: (i32, f64, u8) = (500, 6.4, 1);

    let five_hundred = x.0;
    let six_point_four = x.1;
    let one = x.2;
}

