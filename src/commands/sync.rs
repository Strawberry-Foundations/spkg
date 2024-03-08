use std::sync::{Arc, Mutex};
use std::time::Instant;

use tokio::fs::File;
use tokio::io::AsyncWriteExt;

use futures_util::stream::StreamExt;

use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RED, YELLOW};
use crate::fs::format::format_size;
use crate::net::remote::remote_header;

use crate::spkg_core::{CONFIG, SPKG_DIRECTORIES, STRING_LOADER};
use crate::utilities::delete_last_line;

pub async fn sync() {
    let start_time = Instant::now();

    let success_counter = Arc::new(Mutex::new(0));
    let unsuccess_counter = Arc::new(Mutex::new(0));

    for (name, url) in CONFIG.repositories.iter() {
        let unsuccess_counter_clone = unsuccess_counter.clone();

        let database_repo = format!("{url}/package.db");
        let database_local = format!("{}{name}.db", SPKG_DIRECTORIES.mirrors);
        let content_size = remote_header(&database_repo).await;

        println!("... {} {CYAN}{BOLD}{url}{C_RESET} ({name}) ...{C_RESET}", STRING_LOADER.load("SyncingPackageDatabase"));

        let Ok(response) = reqwest::get(database_repo.clone()).await else {
            delete_last_line();

            eprintln!("{RED}{BOLD} × {C_RESET} {} {CYAN}{BOLD}{url}{C_RESET} ({name}) ...{C_RESET}", STRING_LOADER.load("SyncingPackageDatabase"));
            eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", STRING_LOADER.load("HttpError"));

            let mut counter = unsuccess_counter_clone.lock().unwrap();
            *counter += 1;

            continue
        };

        if response.status().is_success() {
            let mut database = File::create(database_local).await.unwrap_or_else(|_| {
                eprintln!("{CYAN}{BOLD}{}:{C_RESET} {}", SPKG_DIRECTORIES.mirrors, STRING_LOADER.load("MissingPermissions"));
                eprintln!("{}", STRING_LOADER.load("MissingPermissionsPackageDatabaseUpdate"));
                std::process::exit(1);
            });

            let mut stream = response.bytes_stream();

            while let Some(item) = stream.next().await {
                let chunk = item;

                database.write_all(&chunk.unwrap()).await.unwrap_or_else(|_| {
                    eprintln!("{CYAN}{BOLD}{}:{C_RESET} {}", SPKG_DIRECTORIES.mirrors, STRING_LOADER.load("MissingPermissions"));
                    eprintln!("{}", STRING_LOADER.load("MissingPermissionsPackageDatabaseUpdate"));
                    std::process::exit(1);
                });
            }
        }

        else {
            eprintln!("{}{C_RESET}", STRING_LOADER.load("HttpError"));
        }

        delete_last_line();
        println!("{GREEN}{BOLD} ✓ {C_RESET} {} {CYAN}{BOLD}{url}{C_RESET} ({name}) ({}) ...{C_RESET}",
                 STRING_LOADER.load("SyncingPackageDatabase"),
                 format_size(content_size)
        );

        let mut counter = success_counter.lock().unwrap();
        *counter += 1;
    }

    // println!("{}", success_counter.lock().unwrap());
    // println!("{}", unsuccess_counter.lock().unwrap());

    if *unsuccess_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() == 0 {
        eprintln!("{}{C_RESET}", STRING_LOADER.load("UnsuccessfulSyncingPackageDatabase"));
        std::process::exit(1);
    }
    else if *unsuccess_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() >= 1 {
        eprintln!("{YELLOW}{BOLD} ! {C_RESET} {}{C_RESET}", STRING_LOADER.load("AtLeastOneUnsuccessfulSyncingPackageDatabase"));
        println!("{}", STRING_LOADER.load_with_params("SuccessSyncingPackageDatabase", &[&format!("{:.2}", start_time.elapsed().as_secs_f64())]));
    }
    else {
        println!("{}", STRING_LOADER.load_with_params("SuccessSyncingPackageDatabase", &[&format!("{:.2}", start_time.elapsed().as_secs_f64())]));
    }
}