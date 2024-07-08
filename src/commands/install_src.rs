use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};
use crate::core::specfile::fetch_specfile;

async fn do_install(packages: Vec<String>, options: &CommandOptions, mut package_list: PackageList) -> eyre::Result<()> {
    let package = get_package(packages.first().unwrap(), &mut package_list, options)?;
    let data = fetch_specfile(&package.specfile).await;

    if data.srcpkg.is_none() {
        eprintln!("{}", STRINGS.load("PackageNotAvailableAsSrcPkg"));
        std::process::exit(1);
    }


    Ok(())
}

pub async fn install_src(packages: Vec<String>, options: &CommandOptions) -> eyre::Result<()> {
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