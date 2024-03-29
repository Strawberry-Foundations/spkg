# **Advanced Source Package Managment (spkg)**
![version](https://img.shields.io/badge/spkg-2.0.0beta1-success) 
![Code Size](https://img.shields.io/github/languages/code-size/Strawberry-Foundations/spkg)
![Commit activity](https://img.shields.io/github/commit-activity/w/Strawberry-Foundations/spkg)
![License](https://img.shields.io/github/license/Strawberry-Foundations/spkg)

spkg is a package manager that downloads the source code from the official sources, and then mostly compiles it specifically for your device.

The goal of spkg is to get the latest versions of programs easily and 
without much experience, even under distros that do not offer the latest version.
By compiling the package, the program is optimized for your device and can run faster.
So spkg offers you a high security, so you don't have to worry about viruses in packages.

spkg also offers pre-build packages, so you don't have to build big packages like Java yourself. 
<br>

# Setting up
In order to set up spkg for personal use and for development, simply run one of the setup scripts for your system.

### For Ubuntu
```
chmod +x ./scripts/setup_ubuntu.sh
./scripts/setup_ubuntu.sh
```

### For Fedora
```
chmod +x ./scripts/setup_fedora.sh
./scripts/setup_fedora.sh
```

### For other distros
(First install Python 3 & pip)
```
pip install -r ./requirements.txt
```

# Is spkg being developed again?
Yes. We are currently rewriting large parts of spkg's code so that spkg becomes more user friendly. 
Including a new configuration file, better error handling and much more!  

# **Plugins**
spkg offers a convenient plugin system, allowing users to enable advanced features such as installing packages over a secure sandbox! 

## **Sandbox  ![spkg-sandbox](https://img.shields.io/badge/spkg--sandbox-important)**

![spkg-sandbox](https://img.shields.io/badge/spkg--sandbox-2.0.0-informational)
![sandbox-release](https://img.shields.io/badge/Release-stable-success)
![sandbox-methods](https://img.shields.io/badge/Methods-bwrap%2C%20chroot-important)
![sandbox-architetures](https://img.shields.io/badge/Architectures-x86__64%2C%20x86%2C%20aarch64-success)

spkg-sandbox installs packages in a separate environment from the system to provide more security and compatibility. spkg-sandbox works on any system, regardless of the package manager, while spkg without spkg-sandbox currently only works on deb and apk-based systems. It uses Ubuntu 22.04 or 20.04 as base. 
<br>

## **Docker Containers  ![spkg-docker](https://img.shields.io/badge/spkg--docker-important)**

![spkg-docker](https://img.shields.io/badge/spkg--docker-0.1.0-informational)
![docker-release](https://img.shields.io/badge/Release-Not%20released-critical)
![docker-methods](https://img.shields.io/badge/Methods-docker%2C%20podman%20(%3F)-important)
![docker-architetures](https://img.shields.io/badge/Architectures-depending%20on%20docker%20image-success)

spkg-docker installs packages in a Docker container. This provides more security, and is more convenient. Therefore, spkg works on any system that supports docker. The Docker image used is an (custom) Ubuntu 22.04 or 20.04 image.
<br><br>

## **Supported Python Versions**
spkg was built on the basis of Python 3.11. We recommend to use Python 3.10 or higher. All Python versions below 3.9 are untested and therefore not recommended. We do not support Python 3.9 as we use features from a higher Python version. Therefore, please do not open an issue if spkg does not work under Python 3.10 or lower. 

| Version       | Supported | Status                                                    |
| --            | --        | --                                                        | 
| Python 3.8    | No        | ![](https://img.shields.io/badge/-Not_working-orange)     |
| Python 3.9    | No        | ![](https://img.shields.io/badge/-Not_working-orange)     |
| Python 3.10   | Yes       | ![](https://img.shields.io/badge/-Tested,_Working-success)|
| Python 3.11   | Yes       | ![](https://img.shields.io/badge/-Tested,_Working-success)|
| Python 3.12   | Yes       | ![](https://img.shields.io/badge/-Tested,_Working-success)|

## **Linux Support**
Distrobutions and versions that are not listed are not supported by us. 
| Platform  | Version       | Supported     | Branch                                                    | Package Method    |
| --        | --            | --            | --                                                        | --                |   
| coreOS    | 1.0           | Yes           | ![](https://img.shields.io/badge/-Future-orange)          | native, sandbox, docker, copt
| Debian    | 9 and below   | No            | ![](https://img.shields.io/badge/-End_of_Life-red)        | -
| Debian    | 10            | Yes           | ![](https://img.shields.io/badge/-OldOldStable-yellowgreen)| native, sandbox, docker
| Debian    | 11            | Yes           | ![](https://img.shields.io/badge/-OldStable-success)      | native, sandbox, docker
| Debian    | 12            | Yes           | ![](https://img.shields.io/badge/-Stable-success)         | native, sandbox, docker
| Debian    | Sid           | Yes           | ![](https://img.shields.io/badge/-Unstable-orange)        | native, sandbox, docker
| Ubuntu    | 16.04         | No            | ![](https://img.shields.io/badge/-ESM-orange)             | -
| Ubuntu    | 18.04         | Not offical   | ![](https://img.shields.io/badge/-LTS-yellowgreen)        | sandbox, docker
| Ubuntu    | 20.04         | Yes           | ![](https://img.shields.io/badge/-LTS-green)              | native, sandbox, docker
| Ubuntu    | 22.04         | Yes           | ![](https://img.shields.io/badge/-LTS-success)            | native, sandbox, docker
| Ubuntu    | 22.10         | Yes           | ![](https://img.shields.io/badge/-Old_Stable-green)       | native, sandbox, docker
| Ubuntu    | 23.04         | Yes           | ![](https://img.shields.io/badge/-Stable-success)         | native, sandbox, docker
| Alpine    | 3.16.x        | Untested      | ![](https://img.shields.io/badge/-Stable-green)           | native, sandbox, docker
| Alpine    | 3.17.x        | Yes           | ![](https://img.shields.io/badge/-Stable-green)           | native, sandbox, docker
| Alpine    | 3.18.x        | Yes           | ![](https://img.shields.io/badge/-Stable-success)         | native, sandbox, docker
| Fedora    | 37 - 38       | Yes           | ![](https://img.shields.io/badge/-Stable-success)         | (soon native), sandbox, docker
| Arch      | -             | Yes           | ![](https://img.shields.io/badge/-Bleeding%20Edge-blueviolet) | sandbox, docker
| Gentoo    | -             | Untested      | ![](https://img.shields.io/badge/-RR-informational)       | sandbox, docker
