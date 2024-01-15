use std::fs;

pub fn open_file(path: &str) -> String {
    fs::read_to_string(path).expect("Could not read file")
}