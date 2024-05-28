use sqlx::{Pool, Sqlite};
use sqlx::sqlite::SqlitePool;
use stblib::colors::{BOLD, C_RESET, YELLOW};
use crate::core::{SPKG_FILES, STRINGS};

pub struct Database {
    pub connection: Pool<Sqlite>,
    pub location: String,
}

impl Database {
    pub async fn new(path: impl ToString) -> Self {
        let sqlite_db = SqlitePool::connect(&path.to_string()).await.unwrap_or_else(|_| {
            if path.to_string() == SPKG_FILES.world_database {
                eprintln!("{YELLOW}{BOLD} ! {C_RESET}{}{C_RESET}", STRINGS.load("WorldDatabaseNotBuilt"));
                std::process::exit(1);
            }

            eprintln!("{YELLOW}{BOLD} ! {C_RESET}{}{C_RESET}", STRINGS.load("PackageDatabaseNotSynced"));
            std::process::exit(1);
        });

        Self {
            connection: sqlite_db,
            location: path.to_string()
        }
    }
}