use crate::global::SPKG_OPTIONS;

mod cli;
mod global;

fn main() {
    println!("{}", SPKG_OPTIONS.sandbox);
}
