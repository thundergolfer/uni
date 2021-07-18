fn main() {
    let number = 3;

    if number < 5 {
        println!("condition was true");
    } else {
        println!("condition was false");
    }

    if number != 0 {
        println!("Number was something other than zero");
    }

    if number % 4 == 0 {
        println!("number is divisible by 4");
    } else if number % 3 == 0 {
        println!("number is divisible by 3");
    } else if number % 2 == 0 {
        println!("number is divisible by 2");
    } else {
        println!("number is not divisible by 4, 3, or 2");
    }

    let mut counter = 0;
    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };

    println!("The result is {}", result);

    let mut num = 3;
    while num != 0 {
        println!("{}!", num);
        num -= 1;
    }

    println!("LIFTOFF!!!");

    let a = [10, 20, 30, 40, 50];

    for element in a.iter() {
        println!("the value is: {}", element);
    }

    for number in (1..5).rev() {
        println!("{}!", number);
    }
    println!("LIFTOFF!!!");

    twelve_days_of_christmas_lyrics();
}

// Pretty janky, but close enough.
fn twelve_days_of_christmas_lyrics() {
    let parts = [
        "partridge in a pear tree",
        "turtle doves",
        "French hens",
        "calling birds",
        "gold rings",
        "geese a laying",
        "swans a swimming",
        "maids a milking",
        "ladies dancing",
        "lords a leaping",
        "pipers piping",
        "drummers drumming",
    ];

    for day in 1..13 {
        if day == 1 {
            println!("On the {}st day of Christmas my true love gave to me,", day);
        } else if day == 2 {
            println!("On the {}nd day of Christmas my true love gave to me,", day);
        } else {
            println!("On the {}th day of Christmas my true love gave to me,", day);
        }

        for part in (0..day).rev() {
            let first_word = if part == 0 {
                if day > 1 { String::from("And a") } else { String::from("A") }
            } else {
                let s = (part+1).to_string();
                s
            };
            println!("{} {},", first_word, parts[part]);
        }

        println!("");
    }
}
