use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
pub struct Specfile {
    pub package: SpecfilePackage,
    pub srcpkg: Option<SpecfileSrcPkg>,
    pub binpkg: Option<SpecfileBinPkg>,
}

#[derive(Serialize, Deserialize)]
pub struct SpecfilePackage {
    pub name: String,
    pub version: String,
    pub description: String,
    pub author: String,
}

#[derive(Serialize, Deserialize)]
pub struct SpecfileSrcPkg {
    pub compose: String,
}

#[derive(Serialize, Deserialize)]
pub struct SpecfileBinPkg {
    pub x86_64: Option<SpecfileBinPkgArch>,
    pub aarch64: Option<SpecfileBinPkgArch>,
}

#[derive(Serialize, Deserialize)]
pub struct SpecfileBinPkgArch {
    pub url: String
}