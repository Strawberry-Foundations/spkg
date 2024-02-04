#![allow(dead_code)]
use std::time::Duration;
use crate::utilities::delete_last_line;

pub struct Spinner {
    pub text: String,
    pub running: bool,
    pub frames: Vec<&'static str>,
    pub interval: u64,
}

impl Spinner {
    pub fn new(string: String) -> Self {
        Self {
            text: string,
            running: false,
            frames: vec!["[-]", "[\\]", "[|]", "[/]"],
            interval: 200,
        }

    }
    pub async fn start(&mut self) {
        self.running = true;
        let running = self.running;

        while running {
            for frame in &self.frames {
                println!("{}", self.text.replace("%spinner%", frame));
                tokio::time::sleep(Duration::from_millis(self.interval)).await;
                delete_last_line()
            }
        }
    }

    pub async fn stop(&mut self) {
        self.running = false;
    }
}