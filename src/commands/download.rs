use std::env;

use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::package::package_download;
use crate::spkg_core::SPKG_FILES;

pub async fn download() {
    let packages: Vec<String> = env::args().skip(2).collect();

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