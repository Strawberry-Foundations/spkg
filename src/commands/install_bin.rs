use std::env::consts::ARCH;
use stblib::colors::{BOLD, C_RESET, RED};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, Package, PackageList};
use crate::core::specfile::{fetch_specfile, Specfile};

async fn do_install(package: Package, options: &CommandOptions, data: Specfile) -> eyre::Result<()> {
    let binpkg_available = match ARCH {
        "x86_64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.x86_64.is_some()),
        "aarch64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.aarch64.is_some()),
        _ => false,
    };

    if !binpkg_available {
        eprintln!("{RED}{BOLD}{}{C_RESET}", STRINGS.load("PackageNotAvailableAsBinPkg"));
        std::process::exit(1);
    }


    Ok(())
}

pub async fn install_bin(packages: Vec<String>, options: &CommandOptions, data: Option<Specfile>) -> eyre::Result<()> {
    if packages.len() < 2 {
        let mut package_list= PackageList::new(&CONFIG.repositories).await;
        let package = get_package(packages.first().unwrap(), &mut package_list, options)?;
        let data = if let Some(data) = data {
            data
        }
        else {
            fetch_specfile(&package.specfile).await
        };
        do_install(package, options, data).await?;
    }
    else {
        for package in packages {
            let mut package_list= PackageList::new(&CONFIG.repositories).await;
            let package = get_package(&package, &mut package_list, options)?;
            let data = fetch_specfile(&package.specfile).await;

            do_install(package, options, data).await?;
        }
    }
    Ok(())
}