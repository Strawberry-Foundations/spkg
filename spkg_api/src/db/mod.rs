use sqlx::{Pool, Sqlite};
use sqlx::sqlite::SqlitePool;

use crate::core::err::DatabaseError;
use crate::path::files::SpkgFiles;

pub struct Database {
    pub connection: Pool<Sqlite>,
    pub location: String,
}

impl Database {
    pub async fn new(path: impl ToString) -> eyre::Result<Self, DatabaseError> {
        let database = match SqlitePool::connect(&path.to_string()).await {
            Ok(pool) => pool,
            Err(_) => {
                if path.to_string() == SpkgFiles::new().world_database {
                    return Err(DatabaseError::WorldDatabaseNotBuilt)
                };
                return Err(DatabaseError::PackageDatabaseNotSynced)   
            }
        };

        Ok(Self {
            connection: database,
            location: path.to_string()
        })
    }
}