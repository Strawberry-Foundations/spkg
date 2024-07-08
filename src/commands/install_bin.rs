use crate::cli::args::CommandOptions;
use crate::core::CONFIG;
use crate::core::package::PackageList;

async fn do_install(packages: Vec<String>, options: &CommandOptions, mut package_list: PackageList) -> eyre::Result<()> {
    Ok(())    
}

pub async fn install_bin(packages: Vec<String>, options: &CommandOptions) -> eyre::Result<()> {
    let mut package_list = PackageList::new(&CONFIG.repositories).await;

    Ok(())
}