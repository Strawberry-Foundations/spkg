use std::process::exit;
use std::time::Duration;

use rustyline::error::ReadlineError;
use stblib::colors::{BOLD, C_RESET, CYAN};
use tokio::time::sleep;
use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::{SPKG_FILES, STRING_LOADER};

pub async fn build() {
    if SPKG_OPTIONS.build_world {
        let mut line_reader = rustyline::DefaultEditor::new().unwrap();

        let input: String = match line_reader.readline(&STRING_LOADER.load("AskRegenWorld")) {
            Ok(i) => i,
            Err(ReadlineError::Interrupted) => {
                sleep(Duration::from_millis(300)).await;
                exit(0);
            }
            Err(ReadlineError::Eof) => exit(0),
            Err(_) => exit(1),
        };

        if input.to_lowercase() == "yes" || input.to_lowercase() == "ja" {
            println!("{C_RESET}{}", STRING_LOADER.load("BuildingWorldDatabase"));

            std::fs::remove_file(&SPKG_FILES.world_database).unwrap_or_else(|_| {
                eprintln!("{CYAN}{BOLD}{}:{C_RESET} {}", SPKG_FILES.world_database, STRING_LOADER.load("MissingPermissions"));
                eprintln!("{}", STRING_LOADER.load("MissingPermissionsWorldDatabase"));
                exit(1);
            });


            let db = Database::new(&SPKG_FILES.world_database).await;

            sqlx::query(r#"CREATE TABLE "world" ("name" TEXT, "version" INTEGER, "branch" TEXT, "arch" TEXT)"#)
                .execute(&db.connection)
                .await.unwrap();

        }
    }
}