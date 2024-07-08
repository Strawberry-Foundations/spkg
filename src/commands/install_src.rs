use crate::cli::args::CommandOptions;
use crate::core::CONFIG;
use crate::core::package::PackageList;

async fn do_install(packages: Vec<String>, options: &CommandOptions, mut package_list: PackageList) -> eyre::Result<()> {
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