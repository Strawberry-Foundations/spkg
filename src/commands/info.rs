use sqlx::Row;
use stblib::colors::{BOLD, C_RESET, UNDERLINE};

use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::{CONFIG, SPKG_FILES, STRING_LOADER};
use crate::spkg_core::package::Package;

pub async fn info() {
    let mut package: Vec<Package> = vec![];
    
    for (name, _) in CONFIG.repositories.iter() {
        let db_location = &SPKG_FILES.package_database.replace("main.db", format!("{name}.db").as_str());
        let db = Database::new(db_location).await;
        
        let result= sqlx::query("SELECT arch FROM packages where name = ?")
            .bind(&SPKG_OPTIONS.package_name)
            .fetch_all(&db.connection)
            .await.unwrap();

        let arch: String = match result.first() {
            Some(res) => res.get("arch"),
            None => continue
        };

        package = if arch == "all" {
            sqlx::query_as("SELECT * FROM packages where name = ?")
                .bind(&SPKG_OPTIONS.package_name)
                .fetch_all(&db.connection)
                .await.unwrap()
        }
        else {
            sqlx::query_as("SELECT * FROM packages where name = ? AND arch = ?")
                .bind(&SPKG_OPTIONS.package_name)
                .bind(std::env::consts::ARCH)
                .fetch_all(&db.connection)
                .await.unwrap()
        };
    };

    let package = package.first().unwrap_or_else(|| {
        eprintln!("{}", STRING_LOADER.load("PackageNotFound"));
        std::process::exit(1);
    });

    println!("{BOLD}{UNDERLINE}{} {} ({}){C_RESET}", STRING_LOADER.load("PackageInformationTitle"), package.name, package.version);
    println!("{}: {}", STRING_LOADER.load("Name"), package.name);
    println!("{}: {}", STRING_LOADER.load("Version"), package.version);
    println!("{}: {}", STRING_LOADER.load("Branch"), package.branch);
    println!("{}: {}", STRING_LOADER.load("Architecture"), package.arch);
    println!("{}: {}", STRING_LOADER.load("PackageUrl"), package.url);
    println!("{}: {}", STRING_LOADER.load("SpecfileUrl"), package.specfile);


}