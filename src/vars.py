# Base Variables
base_version    = "2.0.0"
version         = "2.0a1+u1"
date            = "20230925"
release_type    = "alpha"
alpha           = True
dev_local       = True
langs           = ["de_DE", "en_US"]

if release_type in ["rc", "beta", "alpha"]:
    version = version + f" ({date})"
    
else: 
    version = version