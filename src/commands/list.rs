use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RESET};

use crate::cli::args::CommandOptions;
use crate::core::CONFIG;
use crate::core::package::{BasePackageList, PackageList};

pub async fn list(options: CommandOptions) {
    if options.installed {
        let packages = BasePackageList::new_local().await;

        for entry in packages {
            println!(
                "{GREEN}{BOLD}{}{C_RESET} ({}) @ {CYAN} {}{RESET}/{}",
                entry.name, entry.version, entry.branch, entry.arch
            );
        }
    }
    
    let mut packages = PackageList::new(&CONFIG.repositories).await;
    
    if let Some(arch) = options.arch {
        packages = packages.filter(|p| p.arch == arch).collect();
    }

    for entry in packages {
        println!(
            "{GREEN}{BOLD}{}{C_RESET} ({}) @ {CYAN} {}{RESET}/{}",
            entry.name, entry.version, entry.branch, entry.arch
        );
    }
}