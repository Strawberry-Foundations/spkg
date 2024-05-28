//! # Argparse
//! Functions for handling the command line interface for spkg

use std::env;
use std::error::Error;

use crate::err::spkg::SpkgError;

pub enum Command {
    Help,
    Err(Box<dyn Error>),
    Install(String, CommandOptions),
    Info(String, CommandOptions),
    List(CommandOptions),
}

#[derive(Default, Debug)]
pub struct CommandOptions {
    pub sandbox: bool,
    pub installed: bool,
}

pub struct Args {
    pub args: Vec<String>,
    pub command: Command,
}


impl Default for Args {
    fn default() -> Self {
        Self::new()
    }
}

impl Args {
    pub fn new() -> Self {
        Self::collect()
    }

    pub fn collect() -> Self {
        let args: Vec<String> = env::args().collect();

        let mut options = CommandOptions::default();
        let mut non_option_args = Vec::new();

        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "-s" | "--sandbox" => options.sandbox = true,
                "--installed" => options.installed = true,
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

        let command = if let Some(cmd) = non_option_args.first() {
            match cmd.as_str() {
                "install" => {
                    if let Some(package) = non_option_args.get(1) {
                        Command::Install(package.to_owned(), options)
                    } else {
                        Command::Err(Box::new(SpkgError::InvalidArgument(String::from("Argument cannot be empty"))))
                    }
                },
                "list" => {
                    
                    Command::List(options)
                }
                _ => Command::Help,
            }
        } else {
            Command::Help
        };

        Self {
            args,
            command
        }
    }
}