use std::env::consts::ARCH;
use std::fs::remove_dir_all;
use libspkg::binpkg::BinPkg;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RED, RESET};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, SPKG_DIRECTORIES, STRINGS};
use crate::core::fs::format_size;
use crate::core::package::{get_package, Package, PackageList};
use crate::core::specfile::{fetch_specfile, Specfile};
use crate::net::http::{file_download, remote_header};
use crate::utilities::{get_basename, get_url_basename};

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

    let (url_base, branch) = &get_url_basename(binpkg_url).unwrap();

    let mut sp = crate::spinners::simple::SimpleSpinner::new();
    sp.start(format!(
        "{BOLD}{}: {CYAN}{url_base}/{branch} {}{C_RESET} ({GREEN}{}{C_RESET}) ...{C_RESET}",
        STRINGS.load("Get"), &get_basename(binpkg_url).unwrap(), format_size(content_size)));

    match file_download(binpkg_url, &format!("{}archives/{}", &SPKG_DIRECTORIES.data, &get_basename(binpkg_url).unwrap())).await {
        Ok(_) => {
            sp.stop();
            println!(
                "{GREEN}{BOLD} ✓ {C_RESET} {BOLD}{}: {CYAN}{url_base}/{branch} {}{C_RESET} ({GREEN}{}{RESET}){C_RESET}    ",
                STRINGS.load("Get"), &get_basename(binpkg_url).unwrap(), format_size(content_size)
            )
        }
        Err(err) => {
            sp.stop();
            eprintln!("{RED}{BOLD} × {C_RESET} {BOLD}{}: {CYAN}{}{C_RESET} ({}) ...{C_RESET}", STRINGS.load("Get"), &binpkg_url, package.name);
            eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", err);
        }
    };

    println!("{} {CYAN}{BOLD}{}{C_RESET}", STRINGS.load("FinishedDownloading"), get_basename(binpkg_url).unwrap());

    let mut sp = crate::spinners::simple::SimpleSpinner::new();
    sp.start(format!(
        "{BOLD}{} {CYAN}{}{C_RESET} ...",
        STRINGS.load("ExtractingPackage"), &get_basename(binpkg_url).unwrap()
    ));

    let _binpkg = BinPkg::extract(format!("{}archives/{}", &SPKG_DIRECTORIES.data, &get_basename(binpkg_url).unwrap()), format!("{}archives/_data", &SPKG_DIRECTORIES.data)).unwrap();

    sp.stop();

    println!(
        "{GREEN}{BOLD} ✓ {C_RESET} {BOLD}{} {CYAN}{}{C_RESET}{C_RESET}      ",
        STRINGS.load("ExtractingPackage"), &get_basename(binpkg_url).unwrap()
    );

    let mut sp = crate::spinners::simple::SimpleSpinner::new();
    sp.start(format!(
        "{BOLD}{} ({CYAN}{}{C_RESET}) ...",
        STRINGS.load("InstallPackage"), &package.name
    ));

    subprocess::Exec::shell(format!("cp -r {}archives/_data/* /", &SPKG_DIRECTORIES.data)).popen().unwrap();

    sp.stop();

    println!(
        "{GREEN}{BOLD} ✓ {C_RESET} {BOLD}{} ({CYAN}{}{C_RESET})      ",
        STRINGS.load("InstallPackage"), &package.name
    );

    remove_dir_all(format!("{}archives/_data", &SPKG_DIRECTORIES.data)).unwrap();

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