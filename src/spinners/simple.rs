use std::io::{self, Write};
use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
use std::thread;
use std::time::Duration;
use stblib::colors::C_RESET;
use terminal_size::{terminal_size, Width};

pub struct SimpleSpinner {
    pub handle: Option<thread::JoinHandle<()>>,
    pub running: Arc<AtomicBool>,
}

impl Default for SimpleSpinner {
    fn default() -> Self {
        SimpleSpinner::new()
    }
}

impl SimpleSpinner {
    pub fn new() -> Self {
        SimpleSpinner {
            handle: None,
            running: Arc::new(AtomicBool::new(false)),
        }
    }

    pub fn start(&mut self, text: impl ToString) {
        let running = self.running.clone();
        let text = text.to_string();
        running.store(true, Ordering::SeqCst);

        self.handle = Some(thread::spawn(move || {
            let spinner_chars = ["\x1b[32m\x1b[1m - \x1b[0m",
                "\x1b[32m\x1b[1m \\ \x1b[0m",
                "\x1b[32m\x1b[1m | \x1b[0m",
                "\x1b[32m\x1b[1m / \x1b[0m"];
            let mut index = 0;
            let max_text_length = terminal_size().map(|(Width(w), _)| w as usize).unwrap_or(80) - 3;

            while running.load(Ordering::SeqCst) {
                let display_text = if text.len() > max_text_length {
                    format!("{} {C_RESET}(...)", &text[..max_text_length - 3])
                } else {
                    text.clone()
                };

                print!("\r{} {}", spinner_chars[index], display_text);
                io::stdout().flush().unwrap();

                index = (index + 1) % spinner_chars.len();
                thread::sleep(Duration::from_millis(100));
            }

            print!("\r ");
            io::stdout().flush().unwrap();
        }));
    }

    pub fn stop(&mut self) {
        self.running.store(false, Ordering::SeqCst);
        if let Some(handle) = self.handle.take() {
            handle.join().unwrap();
        }
    }
}