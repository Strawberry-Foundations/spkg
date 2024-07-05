use std::fmt;
use std::str::FromStr;
use sqlx::{FromRow, Row, Error, Decode, Sqlite, Type};
use sqlx::sqlite::{SqliteRow, SqliteTypeInfo, SqliteValueRef};

#[derive(Debug, Clone)]
pub struct Metadata {
    pub srcpkg: bool,
    pub binpkg: bool,
}

impl FromStr for Metadata {
    type Err = MetadataParseError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut s_bool = false;
        let mut b_bool = false;

        for part in s.split(':') {
            match part {
                "s1" => s_bool = true,
                "s0" => s_bool = false,
                "b1" => b_bool = true,
                "b0" => b_bool = false,
                _ => return Err(MetadataParseError::InvalidFormat),
            }
        }

        Ok(Metadata { srcpkg: s_bool, binpkg: b_bool })
    }
}

#[derive(Debug)]
pub enum MetadataParseError {
    InvalidFormat,
}

impl fmt::Display for MetadataParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            MetadataParseError::InvalidFormat => write!(f, "Invalid format"),
        }
    }
}

impl std::error::Error for MetadataParseError {}

impl<'r> Decode<'r, Sqlite> for Metadata {
    fn decode(value: SqliteValueRef<'r>) -> Result<Self, Box<dyn std::error::Error + Send + Sync>> {
        let s = <&str as Decode<Sqlite>>::decode(value)?;
        Metadata::from_str(s).map_err(|e| Box::new(e) as Box<dyn std::error::Error + Send + Sync>)
    }
}

impl Type<Sqlite> for Metadata {
    fn type_info() -> SqliteTypeInfo {
        <String as Type<Sqlite>>::type_info()
    }
}

impl<'r> FromRow<'r, SqliteRow> for Metadata {
    fn from_row(row: &'r SqliteRow) -> Result<Self, Error> {
        let metadata: String = row.try_get("metadata")?;
        let mut s = false;
        let mut b = false;

        for part in metadata.split(':') {
            match part {
                "s1" => s = true,
                "s0" => s = false,
                "b1" => b = true,
                "b0" => b = false,
                _ => (),
            }
        }

        Ok(Metadata {
            srcpkg: s,
            binpkg: b
        })
    }
}
