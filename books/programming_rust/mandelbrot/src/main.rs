use num::Complex;

fn main() {
    println!("Hello, world!");
}

/// Try to determine if `c` is in the Mandelbrot set, using at most `limit`
/// iterations to decide.
///
/// If `c` is not a member, return `Some(i)`, where `i ` is the nuber of iterations
/// it took for `c` to leave the circle of radius 2 centered on the origin.
/// If `c` seems to be a member (more precisely, if we reached the iteration limit
/// without being able to prove that `c` is not a member)
/// return `None`.
fn escape_time(c: Complex<f64>, limit: usize) -> Option<usize> {
    let mut z = Complex { re: 0.0, im: 0.0 };
    for i in 0..limit {
        // To detect if `z` has left a circle (about the origin) of radius 2,
        // compared the squared distance against 4.0 instead of doing square root,
        // b/c it's faster.
        // ie.
        // re^2 + im^2 = C^2 (avoid square root on C by checking against 4)
        if z.norm_sqr() > 4.0 {
            return Some(i);
        }
        z = z * z + c;
    }

    None
}

fn complex_square_add_loop(c: Complex<f64>) {
    let mut z = Complex { re: 0.0, im: 0.0 };
    loop {
        z = z * z + c;
    }
}
