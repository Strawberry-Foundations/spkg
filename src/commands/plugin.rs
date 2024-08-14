use std::fs;
use std::path::{Path, PathBuf};
use eyre::Report;

use libloading::{Library, Symbol};
use libspkg::plugin::{Plugin, PluginProperties};
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN};

use crate::core::{SPKG_DIRECTORIES, STRINGS};
use crate::err::plugin::PluginError;

pub fn main(args: Vec<String>) -> eyre::Result<()> {
    match args.first().unwrap_or(&String::from("")).as_str() {
        "list" => {
            list()
        }
        "info" => {
            list()
        }
        _ => {
            Ok(())
        }
    }
}

pub fn list() -> eyre::Result<()> {
    let path = format!("{}plugins", &SPKG_DIRECTORIES.system_config);
    let dir_path = Path::new(&path);

    match fs::read_dir(dir_path) {
        Ok(entries) => {
            for entry in entries {
                match entry {
                    Ok(entry) => unsafe {
                        let path = entry.path();
                        if !path.is_dir() {
                            let lib = match Library::new(&path) {
                                Ok(obj) => obj,
                                Err(..) => {
                                    return Err(Report::from(PluginError::PluginLoadError(path.file_name().unwrap().to_str().unwrap().to_string())))
                                }
                            };
                            let create_plugin: Symbol<unsafe extern "C" fn() -> (Box<dyn Plugin>, PluginProperties)> = match lib.get(b"create_plugin") {
                                Ok(symbol) => symbol,
                                Err(..) => {
                                    return Err(Report::from(PluginError::PluginLoadError(path.file_name().unwrap().to_str().unwrap().to_string())))
                                }
                            };
                            let (_plugin, properties) = create_plugin();

                            println!("{BOLD}* {CYAN}{} ({}){C_RESET}", path.file_name().unwrap().to_str().unwrap(), properties.id);
                            println!("   - {}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Name"), properties.name);
                            println!("   - {}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Version"), properties.version);
                            println!("   - {}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("PackageId"), properties.package_id);
                        }
                    }
                    Err(e) => println!("{e}"),
                }
            }
        }
        Err(e) => println!("{e}"),
    }

    Ok(())
}

pub fn register() {

}

pub fn execute() {
    let path = PathBuf::from("./data/etc/spkg/plugins/libexample_plugin.so");
    
    unsafe {
        let lib = Library::new(&path).expect("Could not load library");
        let create_plugin: Symbol<unsafe extern "C" fn() -> (Box<dyn Plugin>, PluginProperties)> = lib.get(b"create_plugin").expect("Could not load symbol");
        let (plugin, properties) = create_plugin();

        println!("Loaded plugin {CYAN}{}{C_RESET}", path.file_name().unwrap().to_str().unwrap());
        println!("Plugin Name: {GREEN}{BOLD}{}{C_RESET}", properties.name);
        println!("Plugin Version: {GREEN}{BOLD}{}{C_RESET}", properties.version);
        println!("Plugin ID: {GREEN}{BOLD}{}{C_RESET}", properties.id);
        println!("Plugin Package ID: {GREEN}{BOLD}{}{C_RESET}\n", properties.package_id);
        plugin.execute(&[String::from("help")]);
    }
}