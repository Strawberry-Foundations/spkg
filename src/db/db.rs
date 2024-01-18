use sqlx::{Pool, Sqlite};
use sqlx::sqlite::SqlitePool;

pub struct Database {
    pub connection: Pool<Sqlite>,
    pub location: String,
}

impl Database {
    pub async fn new(path: impl ToString) -> Self {
        let sqlite_db = SqlitePool::connect(&path.to_string()).await.unwrap_or_else(|_| {
            eprintln!("sqlite::connection_error");
            std::process::exit(1);
        });

        Self {
            connection: sqlite_db,
            location: path.to_string()
        }
    }
}