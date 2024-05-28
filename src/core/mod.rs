mod config;

use lazy_static::lazy_static;
use stblib::strings::Strings;

lazy_static! {
    pub static ref CONFIG: config::Config = config::Config::new();
    pub static ref STRINGS: Strings = Strings::new_with_placeholders(&CONFIG.language, get_language_strings().as_str());
}