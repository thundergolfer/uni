use std::str::FromStr;
use std::env;

fn main() {
    let mut numbers = Vec::new();

    for arg in env::args().skip(1) {
        // Line 1 has pulled in the FromStr trait, which is implemented by u64 type.
        // I think this from_str function is an 'associated function', like a static function in Java.
        // 'The Rust Programming Language' book mentioned it early on.
        numbers.push(u64::from_str(&arg).expect("error parsing argument"));
    }

    if numbers.len() == 0 {
        eprintln!("Usage: gcd NUMBER ...");
        std::process::exit(1);
    }

    let mut d = numbers[0];
    for m in &numbers[1..] {
        d = gcd(d, *m); // Repeatedly apply GCD to the mutable 'd'.
    }

    println!("The greatest common divisor of {:?} is {}", numbers, d);
}

fn gcd(mut n: u64, mut m: u64) -> u64 {
    assert!(n != 0 && m != 0);
    while m != 0 {
        if m < n {
            let t = m;
            m = n;
            n = t;
        }
        m = m % n;
    }
    n
}

#[test]
fn test_gcd() {
    assert_eq!(gcd(14, 15), 1);

    assert_eq!(gcd(2 * 3 * 5 * 11 * 17,
                    3 * 7 * 11 * 13 * 19),
                    3 * 11);
}
