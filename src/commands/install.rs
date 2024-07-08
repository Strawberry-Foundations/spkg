use std::env::consts::ARCH;
use dialoguer::Select;
use dialoguer::theme::ColorfulTheme;
use stblib::colors::{BOLD, RED, GREEN, C_RESET};

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
            println!("{}", STRINGS.load("BinPkgAndSrcPkgAvailable"));

            let selection = Select::with_theme(&ColorfulTheme::default())
                .items(&[STRINGS.load("BinPkg"), STRINGS.load("SrcPkg")])
                .interact()
                .unwrap();

            match selection {
                0 => println!("You selected: Yes"),
                1 => println!("You selected: No"),
                _ => unreachable!(),
            }
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