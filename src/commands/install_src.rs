use crate::cli::args::CommandOptions;
use crate::core::CONFIG;
use crate::core::package::PackageList;

pub async fn install_src(packages: Vec<String>, options: &CommandOptions) -> eyre::Result<()> {
    let mut package_list = PackageList::new(&CONFIG.repositories).await;

    Ok(())
}