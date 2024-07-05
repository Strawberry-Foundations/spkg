use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, UNDERLINE};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};

pub async fn info(package: String, options: CommandOptions) -> eyre::Result<()> {
    let mut packages = PackageList::new(&CONFIG.repositories).await;
    let package = get_package(&package, &mut packages, &options)?;

    println!("{BOLD}{UNDERLINE}{CYAN}{} {} ({}){C_RESET}", STRINGS.load("PackageInformationTitle"), package.name, package.version);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Name"), package.name);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Version"), package.version);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Branch"), package.branch);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Architecture"), package.arch);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("SpecfileUrl"), package.specfile);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("SrcPkgAvailable"), package.metadata.srcpkg);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("BinPkgAvailable"), package.metadata.binpkg);

    Ok(())
}