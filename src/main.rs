use crate::spkg_core::STRING_LOADER;

mod cli;
mod spkg_core;
mod statics;
mod utilities;

fn main() {
    println!("{}", STRING_LOADER.str("Get"));
}
