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

fn main() {
    match ARGS.command.as_str() {
        "install" => {}
        "sync" => commands::sync::sync(),
        _ => println!("{}", STRING_LOADER.str_params("Help", &[&VERSION, &std::env::consts::ARCH])),
    }
}
