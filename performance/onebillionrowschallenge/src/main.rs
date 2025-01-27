///! 1️⃣🐝🏎️ The One Billion Row Challenge.
use std::collections::HashMap;
use std::fs::File;
use std::error::Error;
use std::io::{BufRead, BufReader};

#[derive(Debug)]
struct StationStats {
    count: u64,
    sum: f64,
    min: f64,
    max: f64,
}

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <filepath>", args[0]);
        std::process::exit(1);
    }

    let mut station_stats: HashMap<String, StationStats> = HashMap::new();
    let filepath = &args[1];
    let f = BufReader::with_capacity(131072, File::open(filepath)?);
    // for line in f.lines() {
        // Each line is formatted as: $NAME;$TEMPERATURE.
        // For example: "Goodlettsville;41.6"
        // let line = line?;
        // let line_parts: Vec<&str> = line.split(';').collect();
        // let station_name = line_parts[0];
        // let temperature = line_parts[1].parse::<f64>().unwrap();
        
        // let station_stats = if let Some(stats) = station_stats.get_mut(station_name) {
        //     stats
        // } else {
        //     station_stats.entry(station_name.to_string()).or_insert(StationStats {
        //         count: 0,
        //         sum: 0.0,
        //         min: f64::MAX,
        //         max: f64::MIN,
        //     })
        // };
        // station_stats.count += 1;
        // station_stats.sum += temperature;
        // station_stats.min = if temperature < station_stats.min { temperature } else { station_stats.min };
        // station_stats.max = if temperature > station_stats.max { temperature } else { station_stats.max };
    // }

    // // Print out min/mean/max values per station in alphabetical order.
    // // e.g. {Abha=5.0/18.0/27.4, Abidjan=15.7/26.0/34.1, Abéché=12.1/29.4/35.6, Accra=14.7/26.4/33.1, Addis Ababa=2.1/16.0/24.3, Adelaide=4.1/17.3/29.7, ...}
    // let mut stations: Vec<(&String, &StationStats)> = station_stats.iter().collect();
    // stations.sort_by(|a, b| a.0.cmp(b.0));
    
    // let mut output = String::with_capacity(stations.len() * 30);
    // for (station_name, stats) in stations.iter() {
    //     let mean = stats.sum / stats.count as f64;
    //     output.push_str(&format!("{}={:.1}/{:.1}/{:.1}\n", 
    //         station_name,
    //         stats.min,
    //         mean.round(),
    //         stats.max
    //     ));
    // }
    // println!("{}", output);

    Ok(())
}
