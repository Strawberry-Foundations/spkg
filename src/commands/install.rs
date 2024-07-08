use std::env::consts::ARCH;
use dialoguer::Select;
use dialoguer::theme::{ColorfulTheme};
use stblib::colors::{BOLD, RED};

use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};
use crate::core::specfile::fetch_specfile;
use crate::cli::args::CommandOptions;
use crate::commands::install_bin::install_bin;
use crate::commands::install_src::install_src;

async fn do_install(packages: Vec<String>, options: &CommandOptions, mut package_list: PackageList) -> eyre::Result<()> {
    let package = get_package(packages.first().unwrap(), &mut package_list, options)?;
    let data = fetch_specfile(&package.specfile).await;

    let binpkg_available = match ARCH {
        "x86_64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.x86_64.is_some()),
        "aarch64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.aarch64.is_some()),
        _ => false,
    };

    if binpkg_available && data.srcpkg.is_some() {
        println!("{}", STRINGS.load_with_params("BinPkgAndSrcPkgAvailable", &[&package.name]));

        let theme = ColorfulTheme::default();
        let selector = Select::with_theme(&theme).clear(false).default(0);
        let selection = selector
            .items(&[STRINGS.load("BinPkg"), STRINGS.load("SrcPkg")])
            .interact()
            .unwrap();

        match selection {
            0 => {
                println!("\n{}", STRINGS.load_with_params("PackageWillInstall", &[&STRINGS.load("BinPkg")]));
                install_bin(packages, options).await?;
            },
            1 => {
                println!("\n{}", STRINGS.load_with_params("PackageWillInstall", &[&STRINGS.load("SrcPkg")]));
                install_src(packages, options).await?;
            },
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

    Ok(())
}

pub async fn install(packages: Vec<String>, options: CommandOptions) -> eyre::Result<()> {
    if packages.len() < 2 {
        do_install(packages, &options, PackageList::new(&CONFIG.repositories).await).await?;
    }
    else {
        for package in packages {
            do_install(vec![package], &options, PackageList::new(&CONFIG.repositories).await).await?;
        }
    }
    Ok(())
}