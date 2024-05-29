use sqlx::FromRow;
use std::collections::HashMap;
use eyre::Report;
use crate::cli::args::CommandOptions;
use crate::core::db::Database;
use crate::core::SPKG_FILES;
use crate::err::spkg::SpkgError;

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
    pub packages: Vec<Package>,
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


pub struct BasePackageList {
    pub packages: Vec<BasePackage>
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

pub fn get_package(package: String, mut packages: PackageList, options: CommandOptions) -> eyre::Result<Package> {
    if let Some(arch) = options.arch {
        match packages.find(|p| p.name == package && p.arch == arch) {
            Some(package) => Ok(package),
            None => {
                Err(Report::from(SpkgError::PackageNotFound))
            }
        }
    }
    else {
        match packages.find(|p| p.name == package && (p.arch == "all" || p.arch == std::env::consts::ARCH)) {
            Some(package) => Ok(package),
            None => {
                Err(Report::from(SpkgError::PackageNotFound))
            }
        }
    }
}