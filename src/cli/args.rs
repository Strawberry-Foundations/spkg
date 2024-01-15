//! # Argparse
//! Functions for handling the command line interface for spkg

use std::env;

pub struct Args {
    pub args: Vec<String>,
    pub command: String,
    pub options: Vec<String>,
}

impl Args {
    pub fn new() -> Self {
        Self {
            args: vec![],
            command: String::new(),
            options: vec![],
        }
    }

    pub fn collect(&mut self) -> Vec<String> {
        let args: Vec<String> = env::args().skip(1).collect();

        self.args = args.clone();

        self.command = args.clone().first().unwrap().to_string();

        self.options = env::args().skip(2).collect();

        args
    }
}