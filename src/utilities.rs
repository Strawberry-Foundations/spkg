use std::{fs, io};
use std::io::Write;
use std::path::Path;
use url::Url;
use walkdir::WalkDir;
use crate::core::{CONFIG, SPKG_DIRECTORIES};

pub fn open_file(path: &str) -> String {
    fs::read_to_string(path).expect("Could not read file")
}

pub fn delete_last_line() {
    print!("\x1b[1A");
    print!("\x1b[2K");
    io::stdout().flush().unwrap();
}

pub fn get_language_strings() -> String {
    open_file(format!("{}{}.yml", &SPKG_DIRECTORIES.language_files, CONFIG.language).as_str())
}

pub fn get_basename(path: &str) -> Option<String> {
    let path = Path::new(path);
    path.file_name()?.to_str().map(|s| s.to_string())
}

pub fn get_url_basename(url: &str) -> Result<(String, String), String> {
    match Url::parse(url) {
        Ok(parsed_url) => {
            let scheme = parsed_url.scheme();
            let host = match parsed_url.host_str() {
                Some(host) => host,
                None => return Err("Invalid URL: no host found".to_string()),
            };
            let domain = format!("{}://{}", scheme, host);

            let path_segments: Vec<&str> = parsed_url.path_segments().map_or(Vec::new(), |c| c.collect());
            if path_segments.len() < 2 {
                return Err("Invalid URL: not enough path segments".to_string());
            }
            let branch = path_segments[1].to_string();

            Ok((domain, branch))
        },
        Err(e) => Err(format!("Failed to parse URL: {}", e)),
    }
}

pub fn copy_dir_all(src: impl AsRef<Path>, dst: impl AsRef<Path>) -> std::io::Result<()> {
    fs::create_dir_all(&dst)?;

    for entry in WalkDir::new(&src) {
        let entry = entry?;
        let path = entry.path();
        let relative_path = path.strip_prefix(src.as_ref()).unwrap();
        let dest_path = dst.as_ref().join(relative_path);

        if path.is_dir() {
            fs::create_dir_all(&dest_path)?;
        } else {
            fs::copy(path, &dest_path)?;
        }
    }
    Ok(())
}