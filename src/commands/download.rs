use stblib::colors::{BOLD, C_RESET, UNDERLINE};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};

pub async fn download(package: String, options: CommandOptions) -> eyre::Result<()> {
    let packages = PackageList::new(&CONFIG.repositories).await;
    let package = get_package(package, packages, options).unwrap();

    println!("{BOLD}{UNDERLINE}{} {} ({}){C_RESET}", STRINGS.load("PackageInformationTitle"), package.name, package.version);
    println!("{}: {}", STRINGS.load("Name"), package.name);
    println!("{}: {}", STRINGS.load("Version"), package.version);
    println!("{}: {}", STRINGS.load("Branch"), package.branch);
    println!("{}: {}", STRINGS.load("Architecture"), package.arch);
    println!("{}: {}", STRINGS.load("PackageUrl"), package.url);
    println!("{}: {}", STRINGS.load("SpecfileUrl"), package.specfile);

    Ok(())
}