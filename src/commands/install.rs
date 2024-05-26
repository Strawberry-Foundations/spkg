use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::package::package_download;
use crate::spkg_core::SPKG_FILES;

pub async fn install() {
    let db = Database::new(&SPKG_FILES.package_database).await;

    package_download(&db, &SPKG_OPTIONS.package_name).await;
}