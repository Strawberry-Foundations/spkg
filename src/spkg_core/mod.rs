pub mod config;
pub mod types;

use lazy_static::lazy_static;

lazy_static!(
    pub static ref SPKG_DIRECTORIES: config::SpkgDirectories = config::SpkgDirectories::new();
    pub static ref SPKG_FILES: config::SpkgFiles = config::SpkgFiles::new();
);