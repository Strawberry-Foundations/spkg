use serde::Deserialize;
use serde_yaml::from_str;

use crate::spkg_core::{SPKG_DIRECTORIES, SPKG_FILES};
use crate::utilities::open_file;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub language: String,
    pub language_strings: String,
}

impl Config {
    pub fn new() -> Self {
        let system_config_raw = open_file(&SPKG_FILES.system_config);
        let mut config: Self = from_str(&system_config_raw).unwrap();

        config.language_strings = open_file(format!("{}{}.yml", &SPKG_DIRECTORIES.language_files, config.language).as_str());

        config
    }
}