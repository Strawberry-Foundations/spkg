#!/bin/bash
# Setup script for spkg: Fedora

sudo dnf install -y \
python3 \
python3-pip \
python3-requests \
python3-yaml \
python3-colorama \

# Not the best method
sudo pip install \
halo
