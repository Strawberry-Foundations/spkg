use reqwest::header;

pub async fn remote_header(url: &String) -> u64 {
    let response = match reqwest::Client::new().head(url).send().await {
        Ok(res) => res,
        Err(_) => return 0
    };

    if response.status().is_success() {
        return response.headers().get(header::CONTENT_LENGTH).unwrap().to_str().unwrap().parse().unwrap();
    }

    0
}