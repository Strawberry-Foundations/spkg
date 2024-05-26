use thiserror::Error;

#[derive(Error, Debug)]
pub enum DatabaseError {
    #[error("World database not built")]
    WorldDatabaseNotBuilt,

    #[error("Package database not synced")]
    PackageDatabaseNotSynced
}