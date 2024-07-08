use std::env::consts::ARCH;
use stblib::colors::{BOLD, RED};

use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};
use crate::core::specfile::fetch_specfile;
use crate::cli::args::CommandOptions;
use crate::commands::install_bin::install_bin;
use crate::commands::install_src::install_src;


pub async fn install(packages: Vec<String>, options: CommandOptions) -> eyre::Result<()> {
    let mut package_list = PackageList::new(&CONFIG.repositories).await;

    if packages.len() < 2 {
        let package = get_package(packages.first().unwrap(), &mut package_list, &options)?;
        let data = fetch_specfile(&package.specfile).await;

        let binpkg_available = match ARCH {
            "x86_64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.x86_64.is_some()),
            "aarch64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.aarch64.is_some()),
            _ => false,
        };

        if binpkg_available && data.srcpkg.is_some() {
            println!("Binpkg & srcpkg available")
        }
        else if binpkg_available && data.srcpkg.is_none() {
            install_bin(packages, options).await?;
        }
        else if !binpkg_available && data.srcpkg.is_some() {
            install_src(packages, options).await?;
        }
        else {
            println!("{RED}{BOLD}{}", STRINGS.load("PackageNotAvailable"))
        }
    }
    else {
        for package in packages {
            let package = get_package(&package, &mut package_list, &options)?;
            let data = fetch_specfile(&package.specfile).await;
        }
    }
    Ok(())
}