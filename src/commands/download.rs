use std::env;
use sqlx::Row;
use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::package::Package;
use crate::spkg_core::{SPKG_FILES, STRING_LOADER};

pub async fn download() {
    let packages: Vec<String> = env::args().skip(2).collect();
    // let dir = env::current_dir().unwrap();

    let db = Database::new(&SPKG_FILES.package_database).await;

    if packages.len() <= 1 {
        let package_db = sqlx::query("SELECT * FROM packages where name = ?")
            .bind(&SPKG_OPTIONS.package_name)
            .fetch_all(&db.connection)
            .await.unwrap();

        let package_db = package_db.first().unwrap_or_else(|| {
            eprintln!("{}", STRING_LOADER.str("PackageNotFound"));
            std::process::exit(1);
        });

        let package = Package {
            name: package_db.get("name"),
            version: package_db.get("version"),
            branch: package_db.get("branch"),
            arch: package_db.get("arch"),
            url: package_db.get("url"),
            specfile: package_db.get("specfile"),
            filename: package_db.get("filename"),
        };

        package.download().await;
    }
    else if packages.len() >= 2 {
        for package in packages {
            let package_db = sqlx::query("SELECT * FROM packages where name = ?")
                .bind(package)
                .fetch_all(&db.connection)
                .await.unwrap();

            let package_db = package_db.first().unwrap_or_else(|| {
                eprintln!("{}", STRING_LOADER.str("PackageNotFound"));
                std::process::exit(1);
            });

            let package = Package {
                name: package_db.get("name"),
                version: package_db.get("version"),
                branch: package_db.get("branch"),
                arch: package_db.get("arch"),
                url: package_db.get("url"),
                specfile: package_db.get("specfile"),
                filename: package_db.get("filename"),
            };

            package.download().await;
        }
    }
}