use crate::cli::args::Args;
use crate::global::SPKG_OPTIONS;

mod cli;
mod global;

fn main() {
    let mut args = Args::new();
    args.collect();

    println!("{}", SPKG_OPTIONS.sandbox);
}
