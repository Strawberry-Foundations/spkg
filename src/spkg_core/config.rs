use serde::Deserialize;
use serde_yaml::from_str;

use crate::spkg_core::{CONFIG, SPKG_DIRECTORIES, SPKG_FILES};
use crate::utilities::{open_file, open_file_2};

#[derive(Debug, Deserialize)]
pub struct Config {
    pub language: String,
}

pub fn get_language_strings() -> String {
    open_file_2(format!("{}{}.yml", &SPKG_DIRECTORIES.language_files, CONFIG.language).as_str())
}

impl Config {
    pub fn new() -> Self {
        let system_config_raw = open_file(&SPKG_FILES.system_config);
        let mut config: Self = from_str(&system_config_raw).unwrap();

        config
    }
}