use reqwest::Client;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, UNDERLINE, RED};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};
use crate::core::specfile::{fetch_specfile, Specfile};

pub async fn spec(package: String, options: CommandOptions) -> eyre::Result<()> {
    let mut packages = PackageList::new(&CONFIG.repositories).await;
    let package = get_package(&package, &mut packages, &options)?;
    let data = fetch_specfile(&package.specfile).await;

    println!("{BOLD}{UNDERLINE}{CYAN}{} {} ({}){C_RESET}", STRINGS.load("PackageSpecInformationTitle"), package.name, package.version);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Name"), data.package.name);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Version"), data.package.version);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Description"), data.package.description);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Author"), data.package.author);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("SrcPkgAvailable"), {
        if data.srcpkg.is_some() { STRINGS.load("Yes") } else { format!("{RED}{}", STRINGS.load("No")) }
    });
    if data.srcpkg.is_some() {
        println!("  {}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("ComposeFile"), data.srcpkg.unwrap().compose);
    }
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("BinPkgAvailable"), {
        if data.binpkg.is_some() { STRINGS.load("Yes") } else { format!("{RED}{}", STRINGS.load("No")) }
    });

    if let Some(binpkg) = &data.binpkg {
        if let Some(arch) = &binpkg.x86_64 {
            println!("  x86_64: {GREEN}{BOLD}{}{C_RESET}", arch.url);
        }
        if let Some(arch) = &binpkg.aarch64 {
            println!("  aarch64: {GREEN}{BOLD}{}{C_RESET}", arch.url);
        }
    }

    Ok(())
}