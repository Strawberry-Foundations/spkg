#![allow(unreachable_code)]
use sqlx::FromRow;
use std::collections::HashMap;
use eyre::Report;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RED, RESET};
use crate::cli::args::CommandOptions;
use crate::core::db::Database;
use crate::core::{SPKG_FILES, STRINGS};
use crate::core::fs::format_size;
use crate::err::spkg::SpkgError;
use crate::net::http::{file_download, remote_header};
use crate::spinners::Spinners;
use crate::utilities::delete_last_line;

#[derive(FromRow, Debug, Clone)]
pub struct Package {
    pub name: String,
    pub version: String,
    pub branch: String,
    pub arch: String,
    pub specfile: String,
    pub metadata: String,
    pub binpkg_url: String,
    pub srcpkg_url: String,
}

#[derive(Clone)]
pub struct PackageList {
    pub packages: Vec<Package>,
}


#[derive(FromRow, Debug)]
pub struct BasePackage {
    pub name: String,
    pub version: String,
    pub branch: String,
    pub arch: String,
}

pub struct BasePackageList {
    pub packages: Vec<BasePackage>
}


impl Package {
    pub async fn download(&self) -> eyre::Result<()> {
        let content_size = remote_header(&self.binpkg_url).await;

        println!("Command temporarily disabled");
        std::process::exit(0);
        let mut sp = crate::spinners::Spinner::new(
            Spinners::Line,
            format!(
                "{BOLD}{}: {CYAN}{}{C_RESET} ({GREEN}{}{RESET}) ({}) ...{C_RESET}",
                STRINGS.load("Get"), self.binpkg_url, format_size(content_size), self.name)
        );

        match file_download(&self.binpkg_url, &self.binpkg_url).await {
            Ok(_) => {
                sp.stop_with_message(format!("{GREEN}{BOLD} ✓ {C_RESET} {BOLD}{}: {CYAN}{}{C_RESET} ({GREEN}{}{RESET}) ({}) ...{C_RESET}", STRINGS.load("Get"), self.binpkg_url, format_size(content_size), self.name));
            }
            Err(err) => {
                sp.stop();
                delete_last_line();
                delete_last_line();
                eprintln!("{RED}{BOLD} × {C_RESET} {BOLD}{}: {CYAN}{}{C_RESET} ({}) ...{C_RESET}", STRINGS.load("Get"), self.binpkg_url, self.name);
                eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", err);
            }
        };
        Ok(())
    }
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

        packages.sort_by(|a, b| a.name.cmp(&b.name));

        Self {
            packages
        }
    }

    pub fn get(&self, package_name: String) -> &Package {
        self.packages.iter().find(|package| package.name == package_name).unwrap()
    }
}

impl Iterator for PackageList {
    type Item = Package;

    fn next(&mut self) -> Option<Self::Item> {
        if self.packages.is_empty() {
            None
        } else {
            Some(self.packages.remove(0))
        }
    }
}

impl FromIterator<Package> for PackageList {
    fn from_iter<I: IntoIterator<Item = Package>>(iter: I) -> Self {
        let packages = iter.into_iter().collect();
        PackageList { packages }
    }
}




impl BasePackageList {
    pub async fn new_local() -> Self {
        let db = Database::new(&SPKG_FILES.world_database).await.unwrap();

        let mut packages: Vec<BasePackage> = sqlx::query_as("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
            .fetch_all(&db.connection)
            .await.unwrap();

        packages.sort_by(|a, b| a.name.cmp(&b.name));

        Self {
            packages
        }
    }

    pub fn get(&self, package_name: String) -> &BasePackage {
        self.packages.iter().find(|package| package.name == package_name).unwrap()
    }
}

impl Iterator for BasePackageList {
    type Item = BasePackage;

    fn next(&mut self) -> Option<Self::Item> {
        if self.packages.is_empty() {
            None
        } else {
            Some(self.packages.remove(0))
        }
    }
}

pub fn get_package(package: &String, packages: &mut PackageList, options: &CommandOptions) -> eyre::Result<Package> {
    if let Some(arch) = &options.arch {
        match packages.find(|p| &p.name == package && &p.arch == arch) {
            Some(package) => Ok(package),
            None => {
                Err(Report::from(SpkgError::PackageNotFound))
            }
        }
    }
    else {
        match packages.find(|p| &p.name == package && (p.arch == "all" || p.arch == std::env::consts::ARCH)) {
            Some(package) => Ok(package),
            None => {
                Err(Report::from(SpkgError::PackageNotFound))
            }
        }
    }
}