use sqlx::Row;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RESET};
use crate::db::db::Database;
use crate::spkg_core::SPKG_FILES;

pub async fn list() {
    let db = Database::new(&SPKG_FILES.package_database).await;

    let entries = sqlx::query("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
        .fetch_all(&db.connection)
        .await.unwrap();

    for entry in entries {
        let name: String = entry.get("name");
        let version: String = entry.get("version");
        let branch: String = entry.get("branch");
        let architecture: String = entry.get("arch");

        println!("{GREEN}{BOLD}{name}{C_RESET} ({version}) @ {CYAN} {branch}{RESET}/{architecture}");
    }
}