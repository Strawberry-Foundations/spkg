pub mod files;
pub mod types;
pub mod config;

use lazy_static::lazy_static;
use stblib::strings::Strings;

lazy_static!(
    pub static ref SPKG_DIRECTORIES: files::SpkgDirectories = files::SpkgDirectories::new();
    pub static ref SPKG_FILES: files::SpkgFiles = files::SpkgFiles::new();

    pub static ref STRING_LOADER: Strings = Strings::new();
);