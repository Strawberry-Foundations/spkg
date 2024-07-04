use std::fs;
use std::path::{Path, PathBuf};

use libloading::{Library, Symbol};
use libspkg::plugin::Plugin;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN};

use crate::core::{SPKG_DIRECTORIES, STRINGS};

pub fn main(args: Vec<String>) {
    match args.first().unwrap_or(&String::from("")).as_str() {
        "list" => {
            list()
        }
        "info" => {
            list()
        }
        _ => {}
    }
}

pub fn list() {
    let path = format!("{}plugins", &SPKG_DIRECTORIES.system_config);
    let dir_path = Path::new(&path);

    match fs::read_dir(dir_path) {
        Ok(entries) => {
            for entry in entries {
                match entry {
                    Ok(entry) => unsafe {
                        let path = entry.path();
                        if !path.is_dir() {
                            let lib = Library::new(&path).expect("Could not load library");
                            let create_plugin: Symbol<unsafe extern "C" fn() -> Box<dyn Plugin>> = lib.get(b"create_plugin").expect("Could not load symbol");
                            let plugin = create_plugin();

                            println!("{BOLD}* {CYAN}{} ({}){C_RESET}", path.file_name().unwrap().to_str().unwrap(), plugin.properties().id);
                            println!("   - {}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Name"), plugin.properties().name);
                            println!("   - {}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("Version"), plugin.properties().version);
                            println!("   - {}: {GREEN}{BOLD}{}{C_RESET}", STRINGS.load("PackageId"), plugin.properties().package_id);
                        }
                    }
                    Err(e) => println!("{e}"),
                }
            }
        }
        Err(e) => println!("{e}"),
    }
}

pub fn register() {

}

pub fn execute() {
    let path = PathBuf::from("./data/etc/spkg/plugins/libexample_plugin.so");
    
    unsafe {
        let lib = Library::new(&path).expect("Could not load library");
        let create_plugin: Symbol<unsafe extern "C" fn() -> Box<dyn Plugin>> = lib.get(b"create_plugin").expect("Could not load symbol");
        let plugin = create_plugin();

        println!("Loaded plugin {CYAN}{}{C_RESET}", path.file_name().unwrap().to_str().unwrap());
        println!("Plugin Name: {GREEN}{BOLD}{}{C_RESET}", plugin.properties().name);
        println!("Plugin Version: {GREEN}{BOLD}{}{C_RESET}", plugin.properties().version);
        println!("Plugin ID: {GREEN}{BOLD}{}{C_RESET}", plugin.properties().id);
        println!("Plugin Package ID: {GREEN}{BOLD}{}{C_RESET}\n", plugin.properties().package_id);
        plugin.execute();
    }
}