use std::collections::HashMap;
use serde::Deserialize;
use serde_yaml::from_str;

use crate::err;
use crate::core::{CONFIG, SPKG_DIRECTORIES, SPKG_FILES};
use crate::utilities::open_file;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub language: String,
    pub main_url: String,
    pub build_directory: String,
    pub repositories: HashMap<String, String>,
}



impl Config {
    pub fn new() -> Self {
        let system_config_raw = open_file(&SPKG_FILES.system_config);
        let config: Self = from_str(&system_config_raw).unwrap_or_else(|err| {
            std::process::exit(1);
        });

        config
    }
}