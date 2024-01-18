use reqwest::header;

pub fn remote_header(url: &String) -> String {
    let response = reqwest::blocking::Client::new().head(url).send().unwrap();

    let content_size = if response.status().is_success() {
        response.headers().get(header::CONTENT_LENGTH).unwrap().to_str().unwrap().to_string()
    }
    else {
        "0 kB".to_string()
    };

    content_size
}