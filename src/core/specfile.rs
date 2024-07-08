use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct Specfile {
    pub package: SpecfilePackage,
    pub srcpkg: Option<SpecfileSrcPkg>,
    pub binpkg: Option<SpecfileBinPkg>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SpecfilePackage {
    pub name: String,
    pub version: String,
    pub description: String,
    pub author: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SpecfileSrcPkg {
    pub compose: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SpecfileBinPkg {
    pub x86_64: Option<SpecfileBinPkgArch>,
    pub aarch64: Option<SpecfileBinPkgArch>,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct SpecfileBinPkgArch {
    pub url: String
}