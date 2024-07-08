use std::env::consts::ARCH;
use reqwest::header::ACCEPT_CHARSET;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RED, RESET};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::fs::format_size;
use crate::core::package::{get_package, Package, PackageList};
use crate::core::specfile::{fetch_specfile, Specfile};
use crate::net::http::{file_download, remote_header};
use crate::utilities::{delete_last_line, get_basename};

async fn do_install(package: Package, _options: &CommandOptions, data: Specfile) -> eyre::Result<()> {
    let binpkg_available = match ARCH {
        "x86_64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.x86_64.is_some()),
        "aarch64" => data.binpkg.as_ref().map_or(false, |binpkg| binpkg.aarch64.is_some()),
        _ => false,
    };

    if !binpkg_available {
        eprintln!("{RED}{BOLD}{}{C_RESET}", STRINGS.load("PackageNotAvailableAsBinPkg"));
        std::process::exit(1);
    }

    let binpkg_url = match ARCH {
        "x86_64" => &data.binpkg.as_ref().unwrap().x86_64.as_ref().unwrap().url,
        "aarch64" => &data.binpkg.as_ref().unwrap().aarch64.as_ref().unwrap().url,
        _ => unreachable!(),
    };

    let content_size = remote_header(binpkg_url).await;
    
    let mut sp = crate::spinners::simple::SimpleSpinner::new();
    sp.start(format!(
        "{BOLD}{}: {CYAN}{}{C_RESET} ({GREEN}{}{ACCEPT_CHARSET}) ({}) ...{C_RESET}",
        STRINGS.load("Get"), &binpkg_url, format_size(content_size), package.name));

    match file_download(binpkg_url, &get_basename(binpkg_url).unwrap()).await {
        Ok(_) => {
            sp.stop();
            println!("{GREEN}{BOLD} ✓ {C_RESET} {BOLD}{}: {CYAN}{}{C_RESET} ({GREEN}{}{RESET}) ({}) ...{C_RESET}", STRINGS.load("Get"), &binpkg_url, format_size(content_size), package.name)
        }
        Err(err) => {
            sp.stop();
            delete_last_line();
            delete_last_line();
            eprintln!("{RED}{BOLD} × {C_RESET} {BOLD}{}: {CYAN}{}{C_RESET} ({}) ...{C_RESET}", STRINGS.load("Get"), &binpkg_url, package.name);
            eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", err);
        }
    };


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