use crate::spkg_core::{SPKG_DIRECTORIES, STRING_LOADER};

use stblib::colors::{BOLD, C_RESET, CYAN, RED};


#[derive(Debug, Eq, PartialEq)]
pub enum SpkgError {
    HttpError(&'static String, &'static String),
    MissingPermissions(&'static str),
    ConfigError(String),
}

pub fn throw(error: SpkgError) {
    match error {
        SpkgError::HttpError(url, name) => {
            eprintln!("{RED}{BOLD} × {C_RESET} {} {CYAN}{BOLD}{}{C_RESET} ({}){C_RESET}", STRING_LOADER.load("SyncingPackageDatabase"), url, name);
            eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", STRING_LOADER.load("HttpError"));
        },
        SpkgError::MissingPermissions(suberror) => {
            eprintln!("{CYAN}{BOLD}{}:{C_RESET} {}", SPKG_DIRECTORIES.mirrors, STRING_LOADER.load("MissingPermissions"));
            eprintln!("{}", STRING_LOADER.load(suberror));
        },
        SpkgError::ConfigError(error) => {
            eprintln!("{} ({}){C_RESET}", STRING_LOADER.load("InvalidConfig"), error);
        }
    }
}