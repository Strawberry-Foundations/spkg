use crate::db::db::Database;
use crate::spkg_core::SPKG_FILES;

pub fn sync() {
    let db = Database::new(&SPKG_FILES.package_database);
}