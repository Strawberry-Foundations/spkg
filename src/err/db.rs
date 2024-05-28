use std::error::Error;
use std::fmt::{Display, Formatter, Result};

#[derive(Debug)]
pub enum DatabaseError {
    WorldDatabaseNotBuilt,
    PackageDatabaseNotSynced
}

impl Display for DatabaseError {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            DatabaseError::WorldDatabaseNotBuilt => write!(f, ""),
            DatabaseError::PackageDatabaseNotSynced => write!(f, ""),
        }
    }
}

impl Error for DatabaseError {}
