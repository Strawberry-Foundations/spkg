pub mod files;
pub mod types;
pub mod config;

use lazy_static::lazy_static;
use stblib::strings::Strings;
use crate::spkg_core::config::get_language_strings;

lazy_static!(
    pub static ref CONFIG: config::Config = config::Config::new();
    pub static ref SPKG_DIRECTORIES: files::SpkgDirectories = files::SpkgDirectories::new();
    pub static ref SPKG_FILES: files::SpkgFiles = files::SpkgFiles::new();

    pub static ref STRING_LOADER: Strings = Strings::new_with_placeholders(&CONFIG.language, get_language_strings().as_str());
);