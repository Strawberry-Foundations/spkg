use crate::spkg_core::CONFIG;

pub fn sync() {
    for (name, url) in CONFIG.repositories.iter() {
        let repo = format!("{url}/package.db");

        println!("{repo}");
    }
}