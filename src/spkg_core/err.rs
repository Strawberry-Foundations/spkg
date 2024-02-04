use std::{error, fmt};

#[derive(Debug)]
pub struct SpkgError {
    message: String
}

impl fmt::Display for SpkgError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.message)
    }
}

impl error::Error for SpkgError {}

impl SpkgError {
    pub fn new(message: impl ToString) -> Self {
        Self {
            message: message.to_string()
        }
    }
}