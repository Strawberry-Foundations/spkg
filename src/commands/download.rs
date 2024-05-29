use stblib::colors::{BOLD, C_RESET, UNDERLINE};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};

pub async fn download(package: String, options: CommandOptions) -> eyre::Result<()> {
    let packages = PackageList::new(&CONFIG.repositories).await;
    let package = get_package(package, packages, options)?;
    
    package.download().await?;

    Ok(())
}