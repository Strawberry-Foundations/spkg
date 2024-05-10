use crate::spkg_core::{SPKG_DIRECTORIES, STRING_LOADER};

use stblib::colors::{BOLD, C_RESET, CYAN, RED};


#[derive(Debug, Eq, PartialEq)]
pub enum SpkgError {
    HttpError,
    MissingPermissions(&'static str)
}

pub fn throw(error: SpkgError, params: &[&dyn std::fmt::Display]) {
    match error {
        SpkgError::HttpError => {
            eprintln!("{RED}{BOLD} × {C_RESET} {} {CYAN}{BOLD}{}{C_RESET} ({}){C_RESET}", STRING_LOADER.load("SyncingPackageDatabase"), params[0], params[1]);
            eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", STRING_LOADER.load("HttpError"));
        },
        SpkgError::MissingPermissions(suberror) => {
            eprintln!("{CYAN}{BOLD}{}:{C_RESET} {}", SPKG_DIRECTORIES.mirrors, STRING_LOADER.load("MissingPermissions"));
            eprintln!("{}", STRING_LOADER.load(suberror));
        }
    }
}