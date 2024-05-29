use crate::core::SPKG_DIRECTORIES;
use crate::statics::DEVELOPMENT_MODE;

pub struct SpkgDirectories {
    pub system_config: String,
    pub user_config: String,
    pub data: String,
    pub mirrors: String,
    pub language_files: String,
}

pub struct SpkgFiles {
    pub world_database: String,
    pub package_database: String,
    pub system_config: String,
    pub user_config: String,
    pub lockfile: String,
}

impl SpkgDirectories {
    pub fn new() -> Self {
        let mut directories = Self {
            system_config: "".to_string(),
            user_config: "".to_string(),
            data: "".to_string(),
            mirrors: "".to_string(),
            language_files: "".to_string(),
        };

        if DEVELOPMENT_MODE {
            directories.system_config = String::from("./data/etc/spkg/");
            directories.user_config = String::from("./data/userconfig/spkg/");
            directories.data = String::from("./data/var/lib/spkg/");
            directories.mirrors = String::from("./data/var/lib/spkg/mirrors/");
            directories.language_files = String::from("./data/etc/spkg/lang/");
        }
        else {
            directories.system_config = String::from("/etc/spkg/");
            directories.user_config = String::from("/home/user/.config/spkg/");
            directories.data = String::from("/var/lib/spkg/");
            directories.mirrors = String::from("/var/lib/spkg/mirrors/");
            directories.language_files = String::from("/etc/spkg/lang/");
        }

        directories
    }
}

impl SpkgFiles {
    pub fn new() -> Self {
        Self {
            world_database: format!("{}world.db", SPKG_DIRECTORIES.data),
            package_database: format!("{}main.db", SPKG_DIRECTORIES.mirrors),
            system_config: format!("{}config.yml", SPKG_DIRECTORIES.system_config),
            user_config: format!("{}config.yml", SPKG_DIRECTORIES.user_config),
            lockfile: format!("{}lock", SPKG_DIRECTORIES.data),
        }
    }
}

pub fn format_size(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = 1024 * KB;

    if bytes < KB {
        format!("{} B", bytes)
    } else if bytes < MB {
        format!("{:.1} kB", bytes as f64 / KB as f64)
    } else {
        format!("{:.1} MB", bytes as f64 / MB as f64)
    }
}