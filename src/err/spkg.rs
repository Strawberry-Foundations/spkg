use std::error::Error;
use std::fmt::{Display, Formatter, Result};
use lazy_static::lazy_static;
use stblib::colors::{BOLD, C_RESET, RED};

use crate::core::STRINGS;


#[derive(Debug)]
pub enum SpkgError {
    InvalidArgument(String),
    PackageNotFound(String),
    PackageNotAvailable(String),
    PackageNotAvailableAsBinPkg(String),
    PackageNotAvailableAsSrcPkg(String),
}

lazy_static! {
    pub static ref FORMAT: String = format!("{RED}{BOLD}E: {C_RESET}");
}

impl Display for SpkgError {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            SpkgError::InvalidArgument(..) => {
                write!(f, "{}{}", *FORMAT, STRINGS.load("NoArgument"))
            },
            SpkgError::PackageNotFound(package) => {
                write!(f, "{}{}", *FORMAT, STRINGS.load_with_params("PackageNotFound", &[package]))
            },
            SpkgError::PackageNotAvailable(package) => {
                write!(f, "{}{}", *FORMAT, STRINGS.load_with_params("PackageNotAvailable", &[package]))
            },
            SpkgError::PackageNotAvailableAsBinPkg(package) => {
                write!(f, "{}{}", *FORMAT, STRINGS.load_with_params("PackageNotAvailableAsBinPkg", &[package]))
            },
            SpkgError::PackageNotAvailableAsSrcPkg(package) => {
                write!(f, "{}{}", *FORMAT, STRINGS.load_with_params("PackageNotAvailableAsSrcPkg", &[package]))
            },
        }
    }
}

impl Error for SpkgError {}
