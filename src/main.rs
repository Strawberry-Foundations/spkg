use crate::cli::args::{Args, Command};

pub mod cli;
pub mod err;

#[tokio::main]
async fn main() {
    match Args::new().command {
        Command::Install(package, options) => {
            println!("{package} - {options:?}")
        }
        Command::Err(error) => {
            eprintln!("{error}")

        }
        _ => {}
    }
}