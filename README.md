# **Advanced Source Package Managment (spkg)**
![spkg - v1.4](https://img.shields.io/badge/spkg-1.4_pre--release-success) 
![Code Size](https://img.shields.io/github/languages/code-size/Juliandev02/spkg)
![Commit activity](https://img.shields.io/github/commit-activity/w/Juliandev02/spkg)
![License](https://img.shields.io/github/license/Juliandev02/spkg)

spkg is a package manager that downloads the source code from the official sources, and then mostly compiles it specifically for your device. 

The goal of spkg is to get the latest versions of programs easily and 
without much experience, even under distros that do not offer the latest version.
By compiling the package, the program is optimized for your device and can run faster.
So spkg offers you a high security, so you don't have to worry about viruses in packages.

spkg also offers pre-build packages, so you don't have to build big packages like Java yourself. 


# **Plugins**
spkg offers a convenient plugin system, allowing users to enable advanced features such as installing packages over a secure sandbox! 

## **Sandbox  ![spkg-sandbox](https://img.shields.io/badge/spkg--sandbox-important)**

![spkg-sandbox](https://img.shields.io/badge/spkg--sandbox-1.0.0-informational)
![sandbox-release](https://img.shields.io/badge/Release-stable-success)
![sandbox-methods](https://img.shields.io/badge/Methods-bwrap%2C%20chroot-important)
![sandbox-architetures](https://img.shields.io/badge/Architectures-x86__64%2C%20x86%2C%20aarch64-success)

spkg-sandbox installs packages in a separate environment from the system to provide more security and compatibility. spkg-sandbox works on any system, regardless of the package manager, while spkg without spkg-sandbox currently only works on deb-based systems. It uses Ubuntu 22.04 or 20.04 as base. 

## **Docker Containers  ![spkg-docker](https://img.shields.io/badge/spkg--docker-important)**

![spkg-docker](https://img.shields.io/badge/spkg--docker-0.1.0-informational)
![docker-release](https://img.shields.io/badge/Release-Not%20released-critical)
![docker-methods](https://img.shields.io/badge/Methods-docker%2C%20podman%20(%3F)-important)
![docker-architetures](https://img.shields.io/badge/Architectures-depending%20on%20docker%20image-success)

spkg-docker installs packages in a Docker container. This provides more security, and is more convenient. Therefore, spkg works on any system that supports docker. The Docker image used is an Ubuntu 22.04 or 20.04 image.

