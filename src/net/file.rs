use reqwest::Client;
use std::fs::File;
use std::io::Write;
use crate::spkg_core::err::SpkgError;
use crate::spkg_core::STRING_LOADER;

pub async fn file_download(url: &String, filename: &String) -> anyhow::Result<()> {
    let client = Client::new();
    let response = client.get(url).send().await.map_err(|_| SpkgError::new(STRING_LOADER.str("HttpError")))?;

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