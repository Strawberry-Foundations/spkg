use crate::spkg_core::STRING_LOADER;
use crate::statics::VERSION;

pub fn help() {
    println!("{}", STRING_LOADER.str_params("Help", &[&VERSION, &std::env::consts::ARCH]));
}