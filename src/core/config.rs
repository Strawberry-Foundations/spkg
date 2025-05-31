use std::collections::HashMap;
use serde::Deserialize;
use serde_yaml::from_str;
use crate::core::{FALLBACK_STRINGS, SPKG_FILES};
use crate::utilities::open_file;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub language: String,
    pub main_url: String,
    pub build_directory: String,
    pub old_repo: HashMap<String, String>,
    pub repositories: HashMap<String, RepositoryInfo>,
}

#[derive(Debug, Deserialize)]
#[serde(untagged)]
pub enum AnyArch {
    Single(String),
    List(Vec<String>),
}

impl AnyArch {
    pub fn iter(&self) -> AnyArchIter {
        match self {
            AnyArch::Single(single) => AnyArchIter::Single(Some(single)),
            AnyArch::List(multiple) => AnyArchIter::Multiple(multiple.iter()),
        }
    }
}

pub enum AnyArchIter<'a> {
    Single(Option<&'a String>),
    Multiple(std::slice::Iter<'a, String>),
}

impl<'a> Iterator for AnyArchIter<'a> {
    type Item = &'a String;

    fn next(&mut self) -> Option<Self::Item> {
        match self {
            AnyArchIter::Single(single) => single.take(),
            AnyArchIter::Multiple(multiple) => multiple.next(),
        }
    }
}

#[derive(Debug, Deserialize)]
pub struct RepositoryInfo {
    pub url: String,
    pub arch: AnyArch,
}


impl Default for Config {
    fn default() -> Self {
        Self::new()
    }
}

impl Config {
    pub fn new() -> Self {
        let system_config_raw = open_file(&SPKG_FILES.system_config);
        let config: Self = from_str(&system_config_raw).unwrap_or_else(|_| {
            eprintln!("{}", FALLBACK_STRINGS.load("InvalidConfig"));
            std::process::exit(1);
        });

        config
    }
}