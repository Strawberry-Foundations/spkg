use std::collections::HashMap;
use serde::Deserialize;
use serde_yaml::from_str;

use crate::err;
use crate::err::SpkgError;
use crate::spkg_core::{CONFIG, SPKG_DIRECTORIES, SPKG_FILES};
use crate::utilities::open_file;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub language: String,
    pub main_url: String,
    pub build_directory: String,
    pub repositories: HashMap<String, String>,
}

pub fn get_language_strings() -> String {
    open_file(format!("{}{}.yml", &SPKG_DIRECTORIES.language_files, CONFIG.language).as_str())
}

impl Config {
    pub fn new() -> Self {
        let system_config_raw = open_file(&SPKG_FILES.system_config);
        let config: Self = from_str(&system_config_raw).unwrap_or_else(|err| {
            err::throw(SpkgError::ConfigError(format!("{err}")));
            std::process::exit(1);
        });

        config
    }
}