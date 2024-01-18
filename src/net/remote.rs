use reqwest::header;

pub fn remote_header(url: &String) -> u64 {
    let response = match reqwest::blocking::Client::new().head(url).send() {
        Ok(res) => res,
        Err(_) => return 0
    };

    if response.status().is_success() {
        return response.headers().get(header::CONTENT_LENGTH).unwrap().to_str().unwrap().parse().unwrap();
    }

    0
}