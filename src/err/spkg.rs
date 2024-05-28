use std::error::Error;
use std::fmt::{Display, Formatter, Result};

#[derive(Debug)]
pub enum SpkgError {
    InvalidArgument(String)
}

impl Display for SpkgError {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            SpkgError::InvalidArgument(msg) => write!(f, "Invalid Argument: {}", msg),
        }
    }
}

impl Error for SpkgError {}
