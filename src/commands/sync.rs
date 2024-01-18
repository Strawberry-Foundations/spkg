use std::fs::File;
use std::io::copy;
use std::sync::{Arc, Mutex};
use std::time::Instant;

use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RED, YELLOW};
use crate::net::remote::remote_header;

use crate::spkg_core::{CONFIG, SPKG_DIRECTORIES, STRING_LOADER};
use crate::utilities::delete_last_line;

pub fn sync() {
    let start_time = Instant::now();

    let success_counter = Arc::new(Mutex::new(0));
    let unsuccess_counter = Arc::new(Mutex::new(0));

    for (name, url) in CONFIG.repositories.iter() {
        let unsuccess_counter_clone = unsuccess_counter.clone();

        let database_repo = format!("{url}/package.db");
        let database_local = format!("{}{name}.db", SPKG_DIRECTORIES.mirrors);

        println!("... {} {CYAN}{BOLD}{url}{C_RESET} ({name}) ...{C_RESET}", STRING_LOADER.str("SyncingPackageDatabase"));

        let Ok(mut response) = reqwest::blocking::get(database_repo.clone()) else {
            delete_last_line();

            eprintln!("{RED}{BOLD} × {C_RESET} {} {CYAN}{BOLD}{url}{C_RESET} ({name}) ...{C_RESET}", STRING_LOADER.str("SyncingPackageDatabase"));
            eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", STRING_LOADER.str("HttpError"));

            let mut counter = unsuccess_counter_clone.lock().unwrap();
            *counter += 1;

            continue
        };

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
            eprintln!("{}{C_RESET}", STRING_LOADER.str("HttpError"));
        }

        delete_last_line();
        println!("{GREEN}{BOLD} ✓ {C_RESET} {} {CYAN}{BOLD}{url}{C_RESET} ({name}) {}...{C_RESET}", STRING_LOADER.str("SyncingPackageDatabase"), remote_header(url));

        let mut counter = success_counter.lock().unwrap();
        *counter += 1;
    }

    // println!("{}", success_counter.lock().unwrap());
    // println!("{}", unsuccess_counter.lock().unwrap());

    if *unsuccess_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() == 0 {
        eprintln!("{}{C_RESET}", STRING_LOADER.str("UnsuccessfulSyncingPackageDatabase"));
        std::process::exit(1);
    }
    else if *unsuccess_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() >= 1 {
        eprintln!("{YELLOW}{BOLD} ! {C_RESET} {}{C_RESET}", STRING_LOADER.str("AtLeastOneUnsuccessfulSyncingPackageDatabase"));
        println!("{}", STRING_LOADER.str_params("SuccessSyncingPackageDatabase", &[&format!("{:.2}", start_time.elapsed().as_secs_f64())]));
    }
    else {
        println!("{}", STRING_LOADER.str_params("SuccessSyncingPackageDatabase", &[&format!("{:.2}", start_time.elapsed().as_secs_f64())]));
    }
}