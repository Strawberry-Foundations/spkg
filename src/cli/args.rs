//! # Argparse
//! Functions for handling the command line interface for spkg

use std::env;

#[derive(Default)]
pub enum Command {
    #[default]
    None,
    Err(String),
    Install(String),
    Info(String),
    List,
}

#[derive(Default)]
pub struct CommandOptions {
    pub sandbox: bool,
}

#[derive(Default)]
pub struct Args {
    pub args: Vec<String>,
    pub command: Command,
    pub options: CommandOptions
}


impl Args {
    pub fn new() -> Self {
        let args = Self::collect();
        args
    }

    pub fn collect() -> Self {
        let args: Vec<String> = env::args().collect();
        
        let mut options = CommandOptions::default();
        let mut non_option_args = Vec::new();

        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "-s" | "--sandbox" => {
                    options.sandbox = true;
                }
                _ => {
                    if !args[i].starts_with('-') {
                        non_option_args.push(args[i].clone());
                    } else {
                        eprintln!("Warning: Unrecognized option {}", args[i]);
                    }
                }
            }
            i += 1;
        }

        let command = match non_option_args[0].as_str() {
            "install" => {
                if let Some(package) = non_option_args.get(1) {
                    Command::Install(package.to_owned())
                } else {
                    Command::None
                }
            },
            _ => Command::None,
        };

        Self {
            args,
            command,
            options
        }
    }
}