use std::error::Error;
use std::fmt::{Display, Formatter, Result};

#[derive(Debug)]
pub enum PermissionsError {
    MissingPermissionsPackageDatabaseUpdate,
}

impl Display for PermissionsError {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            PermissionsError::MissingPermissionsPackageDatabaseUpdate => write!(f, ""),
        }
    }
}

impl Error for PermissionsError {}
