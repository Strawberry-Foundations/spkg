use crate::cli::SPKG_OPTIONS;

mod cli;

fn main() {
    println!("{}", SPKG_OPTIONS.sandbox);
}
