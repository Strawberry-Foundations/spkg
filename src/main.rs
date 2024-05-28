use crate::cli::args::{Args, Command};

pub mod cli;
pub mod err;
pub mod commands;
pub mod statics;
mod core;
mod utilities;

#[tokio::main]
async fn main() {
    match Args::new().command {
        Command::Help => {

        }
        Command::Install(package, options) => {
            println!("{package} - {options:?}")
        }
        Command::Err(error) => {
            eprintln!("{error}")

        }
        _ => {}
    }
}