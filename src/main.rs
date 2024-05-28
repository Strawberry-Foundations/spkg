use crate::cli::ARGS;
use crate::cli::args::Command;

pub mod cli;
mod err;

#[tokio::main]
async fn main() {
    match &ARGS.command {
        Command::Install(package) => {
            println!("{package}")
        }
        Command::Info(package) => {
            
        } 
        _ => {}
    }
}
