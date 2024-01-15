use lazy_static::lazy_static;

use crate::cli::args::{Args, SpkgOptions};

lazy_static!(
    pub static ref ARGS: Args = Args::collect();
    pub static ref SPKG_OPTIONS: SpkgOptions = Args::collect().collect_options();
);