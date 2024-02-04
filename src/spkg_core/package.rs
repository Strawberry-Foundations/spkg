use spinoff::{Color, Spinner};
use spinoff::spinners::SpinnerFrames;
use stblib::colors::{BOLD, C_RESET, CYAN, GREEN, RED, RESET};
use crate::fs::format::format_size;
use crate::net::file::file_download;
use crate::net::remote::remote_header;
use crate::spkg_core::STRING_LOADER;
use crate::utilities::delete_last_line;

pub struct Package {
    pub name: String,
    pub version: String,
    pub branch: String,
    pub arch: String,
    pub url: String,
    pub specfile: String,
    pub filename: String,
}

impl Package {
    pub async fn download(&self) {
        let frame = SpinnerFrames {
            frames: vec!["[-]", "[\\]", "[|]", "[/]"],
            interval: 200,
        };

        let content_size = remote_header(&self.url).await;

        let mut spinner = Spinner::new(
            frame,
            format!("{BOLD}{}: {CYAN}{}{C_RESET} ({GREEN}{}{RESET}) ({}) ...{C_RESET}", STRING_LOADER.str("Get"), self.url, format_size(content_size), self.name),
            Color::Green
        );



        match file_download(&self.url, &self.filename).await {
            Ok(_) => {
                spinner.stop();
                delete_last_line();
                println!("{GREEN}{BOLD} ✓ {C_RESET} {BOLD}{}: {CYAN}{}{C_RESET} ({}) ...{C_RESET}", STRING_LOADER.str("Get"), self.url, self.name);
            }
            Err(err) => {
                spinner.stop();
                delete_last_line();
                delete_last_line();
                eprintln!("{RED}{BOLD} × {C_RESET} {BOLD}{}: {CYAN}{}{C_RESET} ({}) ...{C_RESET}", STRING_LOADER.str("Get"), self.url, self.name);
                eprintln!("{RED}{BOLD} ↳  {}{C_RESET}", err);
            }
        };

    }
}