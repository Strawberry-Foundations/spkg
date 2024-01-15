use std::fs;

pub fn open_file(path: &str) -> String {
    fs::read_to_string(path).expect("Could not read file")
}

pub fn open_file_2(path: &str) -> String {
    fs::read_to_string(path).expect("Could not read file 2")
}