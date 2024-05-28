use std::env;

use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::package::{Package, package_download};
use crate::spkg_core::{CONFIG, SPKG_FILES};

pub async fn download() {
    let packages: Vec<String> = env::args().skip(2).collect();

    let mut db_packages: Vec<Package> = vec![];

    for (name, _) in CONFIG.repositories.iter() {
        let db_location = &SPKG_FILES.package_database.replace("main.db", format!("{name}.db").as_str());
        let db = Database::new(db_location).await;

        let pkg: Vec<Package> = 
            sqlx::query_as("SELECT * FROM packages")
                .fetch_all(&db.connection)
                .await.unwrap();

        db_packages.extend(pkg);
    };
    
    let db = Database::new(&SPKG_FILES.package_database).await;

    if packages.len() <= 1 {
        package_download(&db, &SPKG_OPTIONS.package_name).await;
    }
    else if packages.len() >= 2 {
        for package in packages {
            package_download(&db, &package).await;
        }
    }
}