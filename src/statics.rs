use lazy_static::lazy_static;

lazy_static! {
    pub static ref VERSION: String = env!("CARGO_PKG_VERSION").to_string();
}

#[cfg(debug_assertions)]
pub const DEVELOPMENT_MODE: bool = true;

#[cfg(not(debug_assertions))]
pub const DEVELOPMENT_MODE: bool = false;
