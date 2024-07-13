use std::fs::{File, OpenOptions};
use std::io::{Read, Write};
use std::net::TcpStream;
use std::time::Instant;
use std::{collections::HashMap, hint::black_box};

use anyhow::Result;
use computers_are_fast::gen_docs;
use serde::{Deserialize, Serialize};
use sysinfo::System;
use tempfile::tempdir;
use openssl::sha;

const CHOICES: [u64; 10] = [
    1,
    10,
    100,
    1_000,
    10_000,
    100_000,
    1_000_000,
    10_000_000,
    100_000_000,
    1_000_000_000,
];

#[derive(Deserialize, Debug, Serialize)]
struct BenchResult {
    name: String,
    platform: String,
    lang_version: String,
    answer: i32,
    answer_duration_ms: f64,
    estimated_n: u64,
    bench_source: String,
    bench_doc: String,
    hints: Option<Vec<String>>,
    language: Option<String>,
}

struct Bench {
    name: String,
    f: fn(n: u64),
    source: &'static str,
    doc: &'static str,
    hints: Option<Vec<String>>,
}

macro_rules! bnchmrk {
    ($b_name:ident) => {
        bnchmrk!($b_name, None)
    };
    ($b_name:ident, $hints:expr) => {
        Bench {
            name: stringify!($b_name).to_string(),
            f: $b_name,
            source: paste::item! { [<$b_name _src>]() },
            doc: paste::item! { [<$b_name _doc>]() },
            hints: $hints,
        }
    };
}

/// Number to guess: How many iterations of an empty loop can we go through in a second?
#[gen_docs]
fn bench_loop(n: u64) {
    for _ in 0..n {
        black_box(());
    }
}

/// Number to guess: How many entries can we add to a std::HashMap in a second?
#[gen_docs]
fn bench_dict_mutation(n: u64) {
    let mut m = HashMap::new();

    let max_entries = 1000;

    for i in 0..n {
        m.insert(i % max_entries, i);
    }
}

/// Number to guess: How many times can we download google.com in a second?
#[gen_docs]
fn bench_download_webpage(n: u64) {
    for _ in 0..n {
        let mut stream = TcpStream::connect("google.com:80").unwrap();

        let request = "GET / HTTP/1.1\r\nHost: google.com\r\nConnection: close\r\n\r\n";

        stream.write_all(request.as_bytes()).unwrap();

        let mut response = String::new();
        stream.read_to_string(&mut response).unwrap();
    }
}

/// Number to guess: How many times can we start the Python interpreter in a second?
#[gen_docs]
fn bench_run_python(n: u64) {
    for _ in 0..n {
        let mut child = std::process::Command::new("python3")
            .args(["-c", "''"])
            .spawn()
            .expect("failed to execute child");
        let ecode = child.wait().expect("failed to wait on child");
        assert!(ecode.success());
    }
}

/// Number to guess: How many fsync'd files can be created against an SSD in a second?
#[gen_docs]
fn bench_create_files(n: u64) {
    let dir = tempdir().unwrap();
    for i in 0..n {
        let file_path = dir.path().join(format!("{}.txt", i));
        let file = File::create(file_path).unwrap();
        file.sync_all().unwrap();
    }
    let dir_path = dir.path();
    let dir_file = OpenOptions::new().read(true).open(dir_path).unwrap();
    dir_file.sync_all().unwrap();
}

/// Number to guess: How many bytes can we write to an output file in a second?
#[gen_docs]
fn bench_write_to_disk(n: u64) {
    const CHUNK_SIZE: usize = 1_000_000; // 1 megabyte
    let data_chunk: [u8; CHUNK_SIZE] = [b'a'; CHUNK_SIZE];
    let mut f = std::fs::File::create("/tmp/bench-write-to-disk").unwrap();
    let mut bytes_written = 0;
    while bytes_written < n {
        let written = f.write(&data_chunk).unwrap();
        bytes_written += CHUNK_SIZE as u64;
        assert_eq!(written, CHUNK_SIZE, "incomplete disk write");
    }
    f.sync_all().unwrap();
}

/// Number to guess: How many bytes can we write to a string in memory in a second?
#[gen_docs]
fn bench_write_to_memory(n: u64) {
    const CHUNK_SIZE: usize = 1_000_000; // 1 megabyte
    let data_chunk: [u8; CHUNK_SIZE] = [b'a'; CHUNK_SIZE];
    let mut buffer: Vec<u8> = vec![];
    let mut bytes_written = 0;
    while bytes_written < n {
        buffer.extend(&data_chunk);
        bytes_written += CHUNK_SIZE as u64;
    }
    assert!(buffer.len() >= n as usize);
}

/// Number to guess: parse iterations possible within one second. File size is 64KiB.
#[gen_docs]
fn bench_json_parse(n: u64) {
    // NB: reading the 64KiB file is a small constant overhead on each run.
    // WARN: no err handling
    let data = std::fs::read_to_string("message.json").unwrap();
    for _ in 0..n {
        let _json: serde_json::Value = serde_json::from_str(&data).unwrap();
    }
}

/// Number to guess: bytes hashed in one second.
#[gen_docs]
fn bench_sha256_digest(n: u64) {
    let mut h = sha::Sha256::new();
    const CHUNK_SIZE: usize = 10_000;
    let s = "a".repeat(CHUNK_SIZE);
    let mut bytes_hashed: usize = 0;

    while bytes_hashed < (n as usize) {
        h.update(s.as_bytes());
        bytes_hashed += CHUNK_SIZE;
    }

    h.finish();
}

/// Number to guess: bytes written to array in one second.
#[gen_docs]
fn bench_fill_array(n: u64) {
    let n: usize = n as usize;
    let mut a = vec![0u8; n]; // mem alloc
    let mut j: usize = 1;
    for i in 0..n {
        j *= 2;
        if j > n {
            j -= n;
        }
        a[i] = (j % 256) as u8; // Ensure value fits in a byte
    }
    println!("{}", a[n / 7]);
}

/// Number to guess: bytes written to array in one second.
#[gen_docs]
fn bench_fill_array_out_of_order(n: u64) {
    let n: usize = n as usize;
    let mut a = vec![0u8; n];
    let mut jump_around: usize = 1;
    for _ in 0..n {
        jump_around *= 2;
        if jump_around > n {
            jump_around -= n;
        }
        a[jump_around % n] = (jump_around % 256) as u8; // Ensure index and value fit in range
    }
    println!("{}", a[n / 7]);
}

fn snake_number_format(mut z: u64) -> String {
    let mut s = Vec::new();
    while z > 0 {
        if s.len() % 4 == 3 {
            s.push('_');
        }
        s.push(char::from_digit((z % 10) as u32, 10).unwrap());
        z /= 10;
    }

    if s.is_empty() {
        return "0".to_string();
    }

    s.reverse();
    s.into_iter().collect()
}

// Exercises a benchmark by first gathering hardware and OS information
// about the host and then running the bench function against each 'guess'
// option until it reaches the correct answer.

// This function is slow because it runs 5 iterations to confirm the
// correct answer.
fn run_benchmark(b: &Bench) -> BenchResult {
    let name = &b.name;
    let f = b.f;

    println!("running benchmark {}", name);
    let mut answer = None;
    let mut elapsed_ms = std::time::Duration::MAX.as_millis() as u64;
    let mut estimated_n = 0;
    for n in CHOICES {
        let now = Instant::now();

        black_box(f(black_box(n)));

        let elapsed = now.elapsed();
        elapsed_ms = elapsed.as_millis() as u64;
        println!("Elapsed: {:.2?}", elapsed);
        if elapsed_ms > 100 {
            estimated_n = n * 1000 / elapsed_ms;
            // Found answer.
            // If we ran next answer we'd exceed one second.
            // NB: we're assuming that all benchmarks have linear scaling.
            println!(
                "benchmark {} answer: {} (est. exact N={})",
                name,
                snake_number_format(n),
                snake_number_format(estimated_n),
            );
            answer = Some(n);
            break;
        }
    }

    let answer: u64 = answer.unwrap_or(*CHOICES.last().expect("hardcoded non-empty"));

    let platform = format!(
        "{}-{}-{}",
        System::name().unwrap(),
        System::os_version().unwrap(),
        System::cpu_arch().unwrap()
    );

    BenchResult {
        name: name.to_string(),
        platform,
        // NB: only the *minimum* version, not the actual version.
        lang_version: env!("CARGO_PKG_RUST_VERSION").into(),
        answer: answer as i32,
        answer_duration_ms: elapsed_ms as f64,
        estimated_n,
        bench_source: b.source.into(),
        bench_doc: b.doc.into(),
        hints: b.hints.clone(),
        language: Some("rust".into()),
    }
}

fn main() -> Result<()> {
    let benchmarks: [Bench; 1] = [
        // bnchmrk![bench_loop, Some(vec![
        //     "black_box(()) is used only to avoid compiler optimizing out the loop. It adds no run time overhead.".to_string(), 
        //     "A CPU can execute around a few billion instructions per second.".to_string()
        // ])],
        // bnchmrk!(bench_dict_mutation),
        // bnchmrk!(bench_download_webpage),
        // bnchmrk!(bench_run_python, Some(vec![
        //     "This is much less than 100 million :)".to_string(),
        //     "On startup Python reads of 100 files!".into(),
        //     "Before running any code Python executes around 1000 syscalls".into(),
        // ])),
        // bnchmrk!(bench_create_files),
        // bnchmrk!(bench_write_to_disk, Some(vec![
        //     "We make sure everything is sync'd to disk before exiting".to_string(),
        // ])),
        // bnchmrk!(bench_write_to_memory),
        // bnchmrk!(bench_json_parse),
        bnchmrk!(bench_sha256_digest, Some(vec![
            "sha256 is cryptographically secure and slower than md5, siphash, CRC32.".to_string()
        ])),
        // bnchmrk!(bench_fill_array),
        // bnchmrk!(bench_fill_array_out_of_order),
    ];

    let mut results = vec![];
    for b in benchmarks {
        let r = black_box(run_benchmark(&b));
        results.push(r);
    }

    std::fs::write("out.rs.json", serde_json::to_string(&results)?)?;
    Ok(())
}
