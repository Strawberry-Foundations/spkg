# Base Variables
base_version            = "2.0.0"
version                 = "2.0.0beta1"
full_ver                = "v" + version
update_channel          = "dev"
date                    = "20231012"
ver                     = version + "-vacakes"
codename                = "Vanilla Cake"
authors                 = ["Juliandev02", "matteodev8", "Paddyk45"]
api                     = "http://api.strawberryfoundations.xyz/v1/"
langs                   = ["de_DE", "en_US"]
dev_local               = True

if update_channel in ["dev", "beta", "alpha"]:
    version = version + f" ({date})"
    
else: 
    version = version