use std::env::consts::ARCH;
use stblib::colors::{BOLD, C_RESET, RED};
use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};
use crate::core::specfile::fetch_specfile;

async fn do_install(packages: Vec<String>, options: &CommandOptions, mut package_list: PackageList) -> eyre::Result<()> {
    let package = get_package(packages.first().unwrap(), &mut package_list, options)?;
    let data = fetch_specfile(&package.specfile).await;

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

pub async fn install_bin(packages: Vec<String>, options: &CommandOptions) -> eyre::Result<()> {
    if packages.len() < 2 {
        do_install(packages, options, PackageList::new(&CONFIG.repositories).await).await?;
    }
    else {
        for package in packages {
            do_install(vec![package], options, PackageList::new(&CONFIG.repositories).await).await?;
        }
    }
    Ok(())
}