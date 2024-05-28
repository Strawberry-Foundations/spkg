use crate::cli::args::CommandOptions;
use crate::core::CONFIG;
use crate::core::package::PackageList;

pub async fn list(options: CommandOptions) {
    if options.installed {

    }

    let packages = PackageList::new(&CONFIG.repositories).await;
}