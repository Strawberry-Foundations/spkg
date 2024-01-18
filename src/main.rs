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

#[tokio::main]
async fn main() {
    match ARGS.command.as_str() {
        "install" => {}
        "sync" => commands::sync::sync().await,
        "list" => commands::list::list().await,
        _ => println!("{}", STRING_LOADER.str_params("Help", &[&VERSION, &std::env::consts::ARCH])),
    }
}
