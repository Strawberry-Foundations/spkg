use std::{fs, io};
use std::io::Write;

pub fn open_file(path: &str) -> String {
    fs::read_to_string(path).expect("Could not read file")
}

pub fn delete_last_line() {
    print!("\x1b[1A");
    print!("\x1b[2K");
    io::stdout().flush().unwrap();
}