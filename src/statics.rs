pub const VERSION: &str = "3.0.0b2";

#[cfg(debug_assertions)]
pub const DEVELOPMENT_MODE: bool = true;

#[cfg(not(debug_assertions))]
pub const DEVELOPMENT_MODE: bool = false;