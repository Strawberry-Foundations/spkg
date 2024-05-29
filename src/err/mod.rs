pub mod http;
pub mod fs;
pub mod spkg;
pub mod db;

#[macro_export]
macro_rules! throw {
    ($err:expr) => {
        println!("{}", $err)
    };
}