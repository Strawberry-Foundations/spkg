use reqwest::Client;
use serde_yaml::Value;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, UNDERLINE};

use crate::cli::args::CommandOptions;
use crate::core::{CONFIG, STRINGS};
use crate::core::package::{get_package, PackageList};

pub async fn spec(package: String, options: CommandOptions) -> eyre::Result<()> {
    let mut packages = PackageList::new(&CONFIG.repositories).await;
    let package = get_package(&package, &mut packages, &options)?;

    let response = Client::new().get(package.specfile).send().await?;

    if !response.status().is_success() {
        println!("Err not reachable");
        std::process::exit(1)
    }

    let specfile = response.text().await?;

    let data: Value = serde_yaml::from_str(&specfile)?;

    println!("{BOLD}{UNDERLINE}{CYAN}{} {} ({}){C_RESET}", STRINGS.load("PackageSpecInformationTitle"), package.name, package.version);
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Name"), data["package"]["name"].as_str().unwrap());
    println!("{}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Version"), data["package"]["version"].as_str().unwrap());

    Ok(())
}