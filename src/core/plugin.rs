use std::path::PathBuf;
use libloading::{Library, Symbol};
use libspkg::plugin::Plugin;

pub fn load_plugin(plugin_path: &PathBuf) -> Box<dyn Plugin> {
    unsafe {
        let lib = Library::new(plugin_path).expect("Could not load library");
        let create_plugin: Symbol<unsafe extern "C" fn() -> Box<dyn Plugin>> = lib.get(b"create_plugin").expect("Could not load symbol");
        let plugin = create_plugin();

        plugin
    }
}