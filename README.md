# spkg
spkg is a package manager that downloads the source code from the official sources, and then compiles it specifically for your device

The goal of spkg is to get the latest versions of programs easily and 
without much experience, even under distros that do not offer the latest version.
By compiling the package, the program is optimized for your device and can run faster.
So spkg offers you a high security, so you don't have to worry about viruses in packages.
---

## fakeroot
fakeroot is used to install packages without the need of elevated privileges. That means you don't need root permissions to install the packages.

A package can be forced-installed by using the `--user` flag, additionally, you can specify the username with `--user=thomas` (e.g. `/home/thomas/.local/fakeroot`)