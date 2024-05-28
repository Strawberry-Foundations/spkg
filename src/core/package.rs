use sqlx::FromRow;

#[derive(FromRow, Debug)]
pub struct Package {
    pub name: String,
    pub version: String,
    pub branch: String,
    pub arch: String,
    pub url: String,
    pub specfile: String,
    pub filename: String,
}

#[derive(FromRow, Debug)]
pub struct BasePackage {
    pub name: String,
    pub version: String,
    pub branch: String,
    pub arch: String,
}

