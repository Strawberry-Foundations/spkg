//! # Argparse
//! Functions for handling the command line interface for spkg

use std::env;

pub struct SpkgOptions {
    pub sandbox: bool,
}

pub struct Args {
    pub args: Vec<String>,
    pub command: String,
    pub options: SpkgOptions
}


impl Args {
    pub fn collect() -> Self {
        let mut args = Self {
            args: vec![],
            command: "".to_string(),
            options: SpkgOptions { sandbox: false },
        };

        let x: Vec<String> = env::args().collect();

        if x.len() <= 1 {
            return args
        }

        let parser: Vec<String> = env::args().skip(1).collect();

        args.args = parser.clone();

        args.command = parser.clone().first().unwrap().to_string();

        args
    }

    pub fn collect_options(&mut self) -> SpkgOptions {
        let mut spkg_options = SpkgOptions {
            sandbox: false
        };

        // for (_index, arg) in self.args.iter().enumerate() {
        for arg in self.args.iter() {
            match arg.as_str() {
                "-s" | "--sandbox" =>  spkg_options.sandbox = true,
                _ => { }
            }
        }

        spkg_options
    }
}