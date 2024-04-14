use crate::cli::ARGS;
use crate::spkg_core::STRING_LOADER;
use crate::statics::VERSION;

mod cli;
mod spkg_core;
mod statics;
mod utilities;
mod commands;
mod net;
mod fs;
mod db;
mod spinners;

#[tokio::main]
async fn main() {
    match ARGS.command.as_str() {
        "install" => {},
        "remove" => {},
        "reinstall" => {},
        "update" => {},
        "upgrade" => {},
        "sync" => commands::sync::sync().await,
        "info" => commands::info::info().await,
        "list" => commands::list::list().await,
        "download" => commands::download::download().await,
        "build" => commands::build::build().await,
        _ => {
            println!("{}", STRING_LOADER.load_with_params("Help", &[&VERSION, &std::env::consts::ARCH]))
        },
    }
}
