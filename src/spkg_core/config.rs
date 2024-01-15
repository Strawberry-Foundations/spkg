use serde::Deserialize;
use serde_yaml::from_str;

use crate::spkg_core::SPKG_FILES;
use crate::utilities::open_file;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub language: String,
}

impl Config {
    pub fn new() -> Self {
        let system_config_raw = open_file(&SPKG_FILES.system_config);
        let mut config: Self = from_str(&system_config_raw).unwrap();

        config
    }
}