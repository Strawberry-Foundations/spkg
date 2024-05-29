use reqwest::header;
use reqwest::Client;
use std::fs::File;
use std::io::Write;

pub async fn remote_header(url: &String) -> u64 {
    let response = match reqwest::Client::new().head(url).send().await {
        Ok(res) => res,
        Err(_) => return 0
    };

    if response.status().is_success() {
        let headers = match response.headers().get(header::CONTENT_LENGTH) {
            None => return 0,
            Some(header) => header,
        };

        return headers.to_str().unwrap().parse().unwrap_or(0);
    }

    0
}



pub async fn file_download(url: &String, filename: &String) -> eyre::Result<()> {
    let client = Client::new();
    let response = client.get(url).send().await.map_err(|_| .. ).unwrap();

    if response.status().is_success() {
        let mut file = File::create(filename)?;
        let bytes = response.bytes().await?;

        file.write_all(&bytes)?;

        Ok(())
    }
    else {
        Ok(())
    }
}

