use std::fs::{read_dir, remove_file};
use std::sync::{Arc, Mutex};
use std::time::{Instant};
use eyre::Report;

use tokio::fs::File;
use tokio::io::AsyncWriteExt;

use futures_util::stream::StreamExt;

use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, YELLOW};
use crate::cli::args::CommandOptions;

use crate::spinners::{Spinner, Spinners};
use crate::core::{CONFIG, SPKG_DIRECTORIES, STRINGS};
use crate::core::fs::format_size;
use crate::err::fs::PermissionsError;
use crate::net::http::remote_header;
use crate::utilities::delete_last_line;

pub async fn sync(_: CommandOptions) -> eyre::Result<()> {
    let start_time = Instant::now();

    let success_counter = Arc::new(Mutex::new(0));
    let failed_counter = Arc::new(Mutex::new(0));

    let mut existing_databases: Vec<String> = Vec::new();
    let mut configured_databases: Vec<String> = Vec::new();

    for entry in read_dir(&SPKG_DIRECTORIES.mirrors)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_file() {
            if let Some(name) = path.file_name() {
                if let Some(name_str) = name.to_str() {
                    existing_databases.push(name_str.to_string());
                }
            }
        }
    }

    for (name, _) in CONFIG.repositories.iter() {
        configured_databases.push(format!("{name}.db"));
    }

    for database in existing_databases {
        if !configured_databases.contains(&database) {
            remove_file(format!("{}{database}", SPKG_DIRECTORIES.mirrors)).unwrap()
        }
    }

    for (name, url) in CONFIG.repositories.iter() {
        let failed_counter_clone = failed_counter.clone();

        let database_repo = format!("{url}/package.db");
        let database_local = format!("{}{name}.db", SPKG_DIRECTORIES.mirrors);
        let content_size = remote_header(&database_repo).await;

        let mut sp = Spinner::new(
            Spinners::Line, format!(
                "{} {CYAN}{BOLD}{url}{C_RESET} ({name}) ...{C_RESET}",
                STRINGS.load("SyncingPackageDatabase"))
        );

        let Ok(response) = reqwest::get(database_repo.clone()).await else {
            sp.stop_with_message(String::new());
            delete_last_line();

            let mut counter = failed_counter_clone.lock().unwrap();
            *counter += 1;

            continue
        };

        if response.status().is_success() {
            let mut database = match File::create(database_local).await {
                Ok(file) => file,
                Err(_) => {
                    sp.stop_with_message(String::new());
                    delete_last_line();
                    return Err(Report::from(PermissionsError::MissingPermissionsPackageDatabaseUpdate))
                }
            };

            let mut stream = response.bytes_stream();

            while let Some(item) = stream.next().await {
                let chunk = item;

                match database.write_all(&chunk.unwrap()).await {
                    Ok(..) => (),
                    Err(_) => {
                        sp.stop_with_message(String::new());
                        delete_last_line();
                        return Err(Report::from(PermissionsError::MissingPermissionsPackageDatabaseUpdate))
                    }
                }
            }
        }

        else {
            sp.stop_with_message(String::new());
            delete_last_line();

            let mut counter = failed_counter_clone.lock().unwrap();
            *counter += 1;

            continue;
        }

        sp.stop_with_message(format!(
            "{GREEN}{BOLD} ✓ {C_RESET} {} {CYAN}{BOLD}{url}{C_RESET} ({name}) ({}) ...{C_RESET}",
            STRINGS.load("SyncingPackageDatabase"), format_size(content_size)
        ));

        let mut counter = success_counter.lock().unwrap();
        *counter += 1;

    }

    if *failed_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() == 0 {
        eprintln!("{}{C_RESET}", STRINGS.load("UnsuccessfulSyncingPackageDatabase"));
        std::process::exit(1);
    }
    else if *failed_counter.lock().unwrap() >= 1 && *success_counter.lock().unwrap() >= 1 {
        eprintln!("{YELLOW}{BOLD} ! {C_RESET} {}{C_RESET}", STRINGS.load("AtLeastOneUnsuccessfulSyncingPackageDatabase"));
    }

    println!("{}", STRINGS.load_with_params("SuccessSyncingPackageDatabase", &[&format!("{:.2}", start_time.elapsed().as_secs_f64())]));
    Ok(())
}