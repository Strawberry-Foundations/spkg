use libloading::{Library, Symbol};
use libspkg::plugin::Plugin;
use std::path::PathBuf;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN};

pub fn main(args: Vec<String>) {
    println!("{args:?}")
}

pub fn list() {
    
}

pub fn register() {
    
}

pub fn execute() {
    let path = PathBuf::from("/home/julian/Projekte/libspkg/example_plugin/target/release/libexample_plugin.so");
    
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