# **Advanced Source Package Management (spkg)**
![version](https://img.shields.io/badge/spkg-3.0.0b2-success)
![Code Size](https://img.shields.io/github/languages/code-size/Strawberry-Foundations/spkg)
![Commit activity](https://img.shields.io/github/commit-activity/w/Strawberry-Foundations/spkg)
![License](https://img.shields.io/github/license/Strawberry-Foundations/spkg)

spkg is a universal package manager that compiles the source code of a desired package on your computer according to your wishes, in order to achieve the best possible performance and security.

The goal of spkg is to get the latest versions of programs easily and
without much experience, even under distros that do not offer the latest version.
By compiling the package, the program is optimized for your device and can run faster.
So spkg offers you a high security, so you don't have to worry about viruses in packages.

spkg also offers pre-build packages (called binpkg's), so you don't have to build big packages like Java yourself.
<br>

# Setting up
In order to set up spkg for personal use and for development, simply run one of the setup scripts for your system.

*Soon*

# **Plugins**
spkg offers a convenient plugin system, allowing users to enable advanced features such as installing packages over a secure sandbox!

*The plugin system is currently under development due to the Rust rewrite and is therefore very unstable*

## **Linux Support**
Distributions and versions that are not listed are not supported by us.
| Platform      | Version       | Supported     | Branch                                                    | Package Method    |
| --            | --            | --            | --                                                        | --                |   
| Strawberry OS | >=2024.7      | Yes           | ![](https://img.shields.io/badge/-Beta-orange)            | native 
| Debian        | >=11          | Yes           | ![](https://img.shields.io/badge/-Stable-success)         | native
| Debian        | Testing/Sid   | Yes           | ![](https://img.shields.io/badge/-Unstable-orange)        | native
| Ubuntu        | 20.04         | Yes           | ![](https://img.shields.io/badge/-LTS-green)              | native
| Ubuntu        | 22.04         | Yes           | ![](https://img.shields.io/badge/-LTS-green)              | native
| Ubuntu        | 24.04         | Yes           | ![](https://img.shields.io/badge/-LTS-green)              | native
| Alpine        | >=3.18        | Untested      | ![](https://img.shields.io/badge/-Stable-success)         | native
| Fedora        | 40            | Untested      | ![](https://img.shields.io/badge/-Stable-success)         | native
