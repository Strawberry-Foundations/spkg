use sqlx::FromRow;
use std::collections::HashMap;
use crate::core::db::Database;
use crate::core::SPKG_FILES;

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



pub struct PackageList {
    pub packages: Vec<Package>
}

impl PackageList {
    pub async fn new(repo_list: &HashMap<String, String>) -> Self {
        let mut packages: Vec<Package> = vec![];

        for (name, _) in repo_list.iter() {
            let db_location = &SPKG_FILES.package_database.replace("main.db", format!("{name}.db").as_str());
            let db = Database::new(db_location).await.unwrap();

            let pkg: Vec<Package> =
                sqlx::query_as("SELECT * FROM packages")
                    .fetch_all(&db.connection)
                    .await.unwrap();

            packages.extend(pkg);
        }

        Self {
            packages
        }
    }

    pub fn get(&self, package_name: String) -> &Package {
        self.packages.iter().find(|package| package.name == package_name).unwrap()
    }
}