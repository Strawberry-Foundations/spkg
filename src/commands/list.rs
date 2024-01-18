use sqlx::Row;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RESET};
use crate::cli::SPKG_OPTIONS;
use crate::db::db::Database;
use crate::spkg_core::SPKG_FILES;

pub async fn list() {
    let db = if SPKG_OPTIONS.list_installed {
        Database::new(&SPKG_FILES.world_database).await
    }
    else {
        Database::new(&SPKG_FILES.package_database).await
    };

    let entries = if SPKG_OPTIONS.list_custom_arch {
        sqlx::query("SELECT * FROM packages WHERE arch = ? ORDER BY name GLOB '[A-Za-z]*' DESC, name")
            .bind(&SPKG_OPTIONS.list_custom_arch_type)
            .fetch_all(&db.connection)
            .await.unwrap()
    } else {
        sqlx::query("SELECT * FROM packages ORDER BY name GLOB '[A-Za-z]*' DESC, name")
            .fetch_all(&db.connection)
            .await.unwrap()
    };

    for entry in entries {
        let name: String = entry.get("name");
        let version: String = entry.get("version");
        let branch: String = entry.get("branch");
        let architecture: String = entry.get("arch");

        println!("{GREEN}{BOLD}{name}{C_RESET} ({version}) @ {CYAN} {branch}{RESET}/{architecture}");
    }
}