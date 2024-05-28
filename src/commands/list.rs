use spkg_api::repo::packages::PackageList;
use sqlx::FromRow;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RESET};
use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::{CONFIG, SPKG_FILES};

#[derive(FromRow, Debug)]
pub struct SpkgListPackage {
    pub name: String,
    pub version: String,
    pub branch: String,
    pub arch: String,
}


pub async fn list() {
    if SPKG_OPTIONS.list_installed {
        let db = Database::new(&SPKG_FILES.world_database).await;

        let mut packages: Vec<SpkgListPackage> = if SPKG_OPTIONS.list_custom_arch {
            sqlx::query_as("SELECT * FROM packages WHERE arch = ? ORDER BY name GLOB '[A-Za-z]*' DESC, name")
                .bind(&SPKG_OPTIONS.list_custom_arch_type)
                .fetch_all(&db.connection)
                .await.unwrap()
        } else {
            sqlx::query_as("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
                .fetch_all(&db.connection)
                .await.unwrap()
        };

        packages.sort_by(|a, b| a.name.cmp(&b.name));

        for entry in packages {
            println!(
                "{GREEN}{BOLD}{}{C_RESET} ({}) @ {CYAN} {}{RESET}/{}",
                entry.name, entry.version, entry.branch, entry.arch
            )
        }
        
        std::process::exit(0);
    };
    
    let packages = PackageList::new(&CONFIG.repositories).await;
    let mut packages: Vec<SpkgListPackage> = vec![];

    for (name, _) in CONFIG.repositories.iter() {
        let db_location = &SPKG_FILES.package_database.replace("main.db", format!("{name}.db").as_str());
        let db = Database::new(db_location).await;

        let pkg: Vec<SpkgListPackage> = if SPKG_OPTIONS.list_custom_arch {
            sqlx::query_as("SELECT * FROM packages WHERE arch = ? ORDER BY name GLOB '[A-Za-z]*' DESC, name")
                .bind(&SPKG_OPTIONS.list_custom_arch_type)
                .fetch_all(&db.connection)
                .await.unwrap()
        } else {
            sqlx::query_as("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
                .fetch_all(&db.connection)
                .await.unwrap()
        };

        packages.extend(pkg);
    };

    packages.sort_by(|a, b| a.name.cmp(&b.name));

    for entry in packages {
        println!(
            "{GREEN}{BOLD}{}{C_RESET} ({}) @ {CYAN} {}{RESET}/{}",
            entry.name, entry.version, entry.branch, entry.arch
        );
    }
}