use crate::cli::args::CommandOptions;
use crate::core::CONFIG;
use crate::core::package::{get_package, PackageList};

pub async fn download(package: Vec<String>, options: CommandOptions) -> eyre::Result<()> {
    let packages = PackageList::new(&CONFIG.repositories).await;
    
    if package.len() == 1 {
        let package = get_package(&package[0], packages, options)?;
        package.download().await?;
    }
    
    Ok(())
}