use sqlx::Row;
use stblib::colors::{BOLD, C_RESET, UNDERLINE};
use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::{SPKG_FILES, STRING_LOADER};

pub async fn info() {
    let db = Database::new(&SPKG_FILES.package_database).await;

    let result= sqlx::query("SELECT arch FROM packages where name = ?")
        .bind(&SPKG_OPTIONS.package_name)
        .fetch_all(&db.connection)
        .await.unwrap();

    let arch: String = result.first().unwrap_or_else(|| {
        eprintln!("{}", STRING_LOADER.load("PackageNotFound"));
        std::process::exit(1);
    }).get("arch");

    let package = if arch == "all" {
        sqlx::query("SELECT name, version, branch, arch, url, specfile FROM packages where name = ?")
            .bind(&SPKG_OPTIONS.package_name)
            .fetch_all(&db.connection)
            .await.unwrap()
    }
    else {
        sqlx::query("SELECT name, version, branch, arch, url, specfile FROM packages where name = ? AND arch = ?")
            .bind(&SPKG_OPTIONS.package_name)
            .bind(std::env::consts::ARCH)
            .fetch_all(&db.connection)
            .await.unwrap()
    };

    for entry in package {
        let name: String = entry.get("name");
        let version: String = entry.get("version");
        let branch: String = entry.get("branch");
        let arch: String = entry.get("arch");
        let packagefile_url: String = entry.get("url");
        let specfile_url: String = entry.get("specfile");

        println!("{BOLD}{UNDERLINE}{} {name} ({version}){C_RESET}", STRING_LOADER.load("PackageInformationTitle"));
        println!("{}: {name}", STRING_LOADER.load("Name"));
        println!("{}: {version}", STRING_LOADER.load("Version"));
        println!("{}: {branch}", STRING_LOADER.load("Branch"));
        println!("{}: {arch}", STRING_LOADER.load("Architecture"));
        println!("{}: {packagefile_url}", STRING_LOADER.load("PackageUrl"));
        println!("{}: {specfile_url}", STRING_LOADER.load("SpecfileUrl"));
    }


}