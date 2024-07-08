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
        Command::Install(packages, options) => {
            match commands::install::install(packages, options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::InstallBin(packages, options) => {
            match commands::install_bin::install_bin(packages, &options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::InstallSource(packages, options) => {
            match commands::install_src::install_src(packages, &options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }

        Command::Sync(options) => {
            match commands::sync::sync(options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::Info(package, options) => {
            match commands::info::info(package, options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::Spec(package, options) => {
            match commands::spec::spec(package, options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::List(options) => {
            commands::list::list(options).await;
        }
        Command::Download(packages, options) => {
            match commands::download::download(packages, options).await {
                Ok(..) => (),
                Err(err) => throw!(err)
            }
        }
        Command::Dummy => {
            commands::plugin::execute()
        }
        Command::Plugin(args) => {
            commands::plugin::main(args)
        }
        Command::Err(error) => {
            eprintln!("{error}")
        }
    }
}