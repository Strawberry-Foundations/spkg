use std::error::Error;
use std::fmt::{Display, Formatter, Result};
use crate::core::STRINGS;

#[derive(Debug)]
pub enum SpkgError {
    InvalidArgument(String),
    PackageNotFound
}

impl Display for SpkgError {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            SpkgError::InvalidArgument(..) => write!(f, "{}", STRINGS.load("NoArgument")),
            SpkgError::PackageNotFound => write!(f, "{}", STRINGS.load("PackageNotFound")),
        }
    }
}

impl Error for SpkgError {}
