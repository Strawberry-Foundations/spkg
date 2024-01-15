use crate::cli::ARGS;

mod cli;
mod spkg_core;
mod statics;
mod utilities;
mod commands;

fn main() {
    match ARGS.command.as_str() {
        "install" => {}
        _ => commands::help::help(),
    }
}
