use crate::cli::args::Args;
mod cli;

fn main() {
    let mut args = Args::new();
    args.collect();

    println!("{}", args.command);
    println!("{:?}", args.options);
}
