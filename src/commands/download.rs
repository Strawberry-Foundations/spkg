use eyre::Report;
use stblib::colors::{BOLD, C_RESET, UNDERLINE};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::PackageList;
use crate::err::spkg::SpkgError;

pub async fn download(package: String, options: CommandOptions) -> eyre::Result<()> {
    let mut packages = PackageList::new(&CONFIG.repositories).await;

    let package = if let Some(arch) = options.arch {
        match packages.find(|p| p.name == package && p.arch == arch) {
            Some(package) => package,
            None => {
                return Err(Report::from(SpkgError::PackageNotFound))
            }
        }
    }
    else {
        match packages.find(|p| p.name == package && (p.arch == "all" || p.arch == std::env::consts::ARCH)) {
            Some(package) => package,
            None => {
                return Err(Report::from(SpkgError::PackageNotFound))
            }
        }
    };

    println!("{BOLD}{UNDERLINE}{} {} ({}){C_RESET}", STRINGS.load("PackageInformationTitle"), package.name, package.version);
    println!("{}: {}", STRINGS.load("Name"), package.name);
    println!("{}: {}", STRINGS.load("Version"), package.version);
    println!("{}: {}", STRINGS.load("Branch"), package.branch);
    println!("{}: {}", STRINGS.load("Architecture"), package.arch);
    println!("{}: {}", STRINGS.load("PackageUrl"), package.url);
    println!("{}: {}", STRINGS.load("SpecfileUrl"), package.specfile);

    Ok(())
}