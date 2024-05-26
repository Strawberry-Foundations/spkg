pub mod core;
pub mod repo;
pub mod db;
pub mod path;

pub const DEVELOPMENT_MODE: bool = true;

use lazy_static::lazy_static;
use crate::path::files::{SpkgDirectories, SpkgFiles};

lazy_static!(
    pub static ref SPKG_DIRECTORIES: SpkgDirectories = SpkgDirectories::new();
    pub static ref SPKG_FILES: SpkgFiles = SpkgFiles::new();
);