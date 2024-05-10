use std::sync::{Arc, Mutex};
use std::time::{Instant};

use tokio::fs::File;
use tokio::io::AsyncWriteExt;

use futures_util::stream::StreamExt;

use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, YELLOW};

use crate::err;
use crate::err::SpkgError;
use crate::spinners::{Spinner, Spinners};
use crate::fs::format::format_size;
use crate::net::remote::remote_header;
use crate::spkg_core::{CONFIG, SPKG_DIRECTORIES, STRING_LOADER};
use crate::utilities::delete_last_line;

pub async fn sync() {
    let start_time = Instant::now();

    let success_counter = Arc::new(Mutex::new(0));
    let failed_counter = Arc::new(Mutex::new(0));

    for (name, url) in CONFIG.repositories.iter() {
        let failed_counter_clone = failed_counter.clone();

        let database_repo = format!("{url}/package.db");
        let database_local = format!("{}{name}.db", SPKG_DIRECTORIES.mirrors);
        let content_size = remote_header(&database_repo).await;

        let mut sp = Spinner::new(
            Spinners::Line, format!(
                "{} {CYAN}{BOLD}{url}{C_RESET} ({name}) ...{C_RESET}",
                STRING_LOADER.load("SyncingPackageDatabase"))
        );

        let Ok(response) = reqwest::get(database_repo.clone()).await else {
            sp.stop_with_message(String::new());
            delete_last_line();
            err::throw(SpkgError::HttpError(url, name));

            let mut counter = failed_counter_clone.lock().unwrap();
            *counter += 1;

            continue
        };

        if response.status().is_success() {
            let mut database = File::create(database_local).await.unwrap_or_else(|_| {
                sp.stop_with_message(String::new());
                delete_last_line();
                err::throw(SpkgError::MissingPermissions("MissingPermissionsPackageDatabaseUpdate"));
                std::process::exit(1);
            });

            let mut stream = response.bytes_stream();

            while let Some(item) = stream.next().await {
                let chunk = item;

                database.write_all(&chunk.unwrap()).await.unwrap_or_else(|_| {
                    sp.stop_with_message(String::new());
                    delete_last_line();
                    err::throw(SpkgError::MissingPermissions("MissingPermissionsPackageDatabaseUpdate"));
                    std::process::exit(1);
                });
            }
        }

        else {
            sp.stop_with_message(String::new());
            delete_last_line();
            err::throw(SpkgError::HttpError(url, name));

            let mut counter = failed_counter_clone.lock().unwrap();
            *counter += 1;
            
            continue;
        }

        sp.stop_with_message(format!(
            "{GREEN}{BOLD} ✓ {C_RESET} {} {CYAN}{BOLD}{url}{C_RESET} ({name}) ({}) ...{C_RESET}", 
            STRING_LOADER.load("SyncingPackageDatabase"), format_size(content_size)
            ));

        let mut counter = success_counter.lock().unwrap();
        *counter += 1;

    }

    if *failed_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() == 0 {
        eprintln!("{}{C_RESET}", STRING_LOADER.load("UnsuccessfulSyncingPackageDatabase"));
        std::process::exit(1);
    }
    else if *failed_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() >= 1 {
        eprintln!("{YELLOW}{BOLD} ! {C_RESET} {}{C_RESET}", STRING_LOADER.load("AtLeastOneUnsuccessfulSyncingPackageDatabase"));
    }
    
    println!("{}", STRING_LOADER.load_with_params("SuccessSyncingPackageDatabase", &[&format!("{:.2}", start_time.elapsed().as_secs_f64())]));
}