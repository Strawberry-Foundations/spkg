use lazy_static::lazy_static;

use crate::cli::args::Args;

pub mod args;

lazy_static! {
    pub static ref ARGS: Args = Args::new();
}