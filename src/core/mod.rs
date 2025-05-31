pub mod config;
pub mod fs;
pub mod package;
pub mod db;
pub mod plugin;
pub mod metadata;
pub mod specfile;

use lazy_static::lazy_static;
use stblib::strings::Strings;
use crate::utilities::{get_language_strings, open_file};

lazy_static! {
    pub static ref SPKG_DIRECTORIES: fs::SpkgDirectories = fs::SpkgDirectories::new();
    pub static ref SPKG_FILES: fs::SpkgFiles = fs::SpkgFiles::new();

    pub static ref CONFIG: config::Config = config::Config::new();
    pub static ref STRINGS: Strings = Strings::new_with_placeholders(&CONFIG.language, get_language_strings().as_str());
    
    pub static ref FALLBACK_STRINGS: Strings = {
        let string_file = open_file(format!("{}{}.yml", &SPKG_DIRECTORIES.language_files, "en_US").as_str());
        Strings::new_with_placeholders("en_US", string_file.as_str())
    };
}