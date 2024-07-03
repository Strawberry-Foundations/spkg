use libloading::{Library, Symbol};
use libspkg::plugin::Plugin;
use std::path::PathBuf;

pub fn execute() {
    let plugin_path = PathBuf::from("/home/julian/Projekte/libspkg/example_plugin/target/release/libexample_plugin.so");
    
    unsafe {
        let lib = Library::new(plugin_path).expect("Could not load library");
        let create_plugin: Symbol<unsafe extern "C" fn() -> Box<dyn Plugin>> = lib.get(b"create_plugin").expect("Could not load symbol");
        let plugin = create_plugin();

        println!("Loaded plugin: {}", plugin.properties().name);
        plugin.execute();
    }
}