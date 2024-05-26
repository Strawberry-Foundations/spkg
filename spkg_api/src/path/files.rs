use crate::DEVELOPMENT_MODE;

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
        let dirs = SpkgDirectories::new();
        Self {
            world_database: format!("{}world.db", dirs.data),
            package_database: format!("{}main.db", dirs.mirrors),
            system_config: format!("{}config.yml", dirs.system_config),
            user_config: format!("{}config.yml", dirs.user_config),
            lockfile: format!("{}lock", dirs.data),
        }
    }
}