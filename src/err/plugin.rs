use std::error::Error;
use std::fmt::{Display, Formatter, Result};
use lazy_static::lazy_static;
use stblib::colors::{BOLD, C_RESET, RED};

use crate::core::STRINGS;


#[derive(Debug)]
pub enum PluginError {
    PluginLoadError(String),
    InvalidPlugin(String),
}

lazy_static! {
    pub static ref FORMAT: String = format!("{RED}{BOLD}E: {C_RESET}");
}

impl Display for PluginError {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            PluginError::PluginLoadError(plugin) => {
                write!(f, "{}{}", *FORMAT, STRINGS.load_with_params("PluginLoadError", &[plugin]))
            },
            PluginError::InvalidPlugin(plugin) => {
                write!(f, "{}{}", *FORMAT, STRINGS.load_with_params("InvalidPlugin", &[plugin]))
            },
        }
    }
}

impl Error for PluginError {}
