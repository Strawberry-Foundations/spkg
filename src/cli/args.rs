//! # Argparse
//! Functions for handling the command line interface for spkg

use std::env;

#[derive(Default)]
pub struct SpkgOptions{
    pub package_name: String,
    pub sandbox: bool,
    pub list_installed: bool,
    pub list_custom_arch: bool,
    pub list_custom_arch_type: String,
    pub build_world: bool,
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
            options: SpkgOptions {
                ..Default::default()
            },
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
            ..Default::default()
        };

        for (index, arg) in self.args.iter().enumerate() {
            match arg.as_str() {
                "-s" | "--sandbox" =>  spkg_options.sandbox = true,
                "-i" | "--installed" => spkg_options.list_installed = true,
                "-a" | "--arch" => {
                    spkg_options.list_custom_arch = true;
                    spkg_options.list_custom_arch_type = self.args.get(index + 1).unwrap_or(&env::consts::ARCH.to_string()).to_owned();
                },
                "world" => spkg_options.build_world = true,
                _ => spkg_options.package_name = self.args.get(index).unwrap().to_owned(),
            }
        }

        spkg_options
    }
}