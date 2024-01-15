use std::fs::File;
use std::io::copy;

use stblib::colors::{BOLD, C_RESET, CYAN};

use crate::spkg_core::{CONFIG, SPKG_DIRECTORIES, STRING_LOADER};

pub fn sync() {
    for (name, url) in CONFIG.repositories.iter() {
        let database_repo = format!("{url}/package.db");
        let database_local = format!("{}{name}.db", SPKG_DIRECTORIES.mirrors);

        println!("{} {CYAN}{BOLD}{url}{C_RESET} ({name}) ...{C_RESET}", STRING_LOADER.str("SyncingPackageDatabase"));

        let mut response = reqwest::blocking::get(database_repo).unwrap_or_else(|_| {
            eprintln!("{}", STRING_LOADER.str("HttpError"));
            std::process::exit(1)
        });

        if response.status().is_success() {
            let mut database = File::create(database_local).unwrap_or_else(|_| {
                eprintln!("{CYAN}{BOLD}{}:{C_RESET} {}", SPKG_DIRECTORIES.mirrors, STRING_LOADER.str("MissingPermissions"));
                eprintln!("{}", STRING_LOADER.str("MissingPermissionsPackageDatabaseUpdate"));
                std::process::exit(1);
            });

            copy(&mut response, &mut database).unwrap_or_else(|_| {
                eprintln!("{CYAN}{BOLD}{}:{C_RESET} {}", SPKG_DIRECTORIES.mirrors, STRING_LOADER.str("MissingPermissions"));
                eprintln!("{}", STRING_LOADER.str("MissingPermissionsPackageDatabaseUpdate"));
                std::process::exit(1);
            });

        }
        else {
            eprintln!("{}", STRING_LOADER.str("HttpError"));
            std::process::exit(1)
        }
    }

    println!("{}", STRING_LOADER.str("SuccessSyncingPackageDatabase"));
}