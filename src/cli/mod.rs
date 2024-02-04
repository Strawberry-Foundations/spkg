pub mod args;
pub mod spinner;

use lazy_static::lazy_static;

lazy_static!(
    pub static ref ARGS: args::Args = args::Args::collect();
    pub static ref SPKG_OPTIONS: args::SpkgOptions = args::Args::collect().collect_options();
);