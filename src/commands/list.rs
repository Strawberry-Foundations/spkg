use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RESET};
use crate::cli::args::CommandOptions;
use crate::core::CONFIG;
use crate::core::package::PackageList;

pub async fn list(options: CommandOptions) {
    if options.installed {

    }

    let packages = PackageList::new(&CONFIG.repositories).await;

    for entry in packages {
        println!(
            "{GREEN}{BOLD}{}{C_RESET} ({}) @ {CYAN} {}{RESET}/{}",
            entry.name, entry.version, entry.branch, entry.arch
        );
    }

}