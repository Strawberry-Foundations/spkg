#![allow(dead_code)]

use crate::cli::args::{Args, Command};
use crate::core::STRINGS;
use crate::statics::VERSION;

pub mod cli;
pub mod err;
pub mod commands;
pub mod statics;
pub mod core;
pub mod utilities;
pub mod spinners;
pub mod net;

#[tokio::main]
async fn main() {
    match Args::new().command {
        Command::Help => {
            println!("{}", STRINGS.load_with_params("Help", &[&VERSION, &std::env::consts::ARCH]))
        }
        Command::Install(package, options) => {
            println!("{package} - {options:?}")
        }
        Command::Info(package, options) => {
            match commands::info::info(package, options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::List(options) => {
            commands::list::list(options).await;
        }
        Command::Sync(options) => {
            match commands::sync::sync(options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::Err(error) => {
            eprintln!("{error}")
        }
    }
}