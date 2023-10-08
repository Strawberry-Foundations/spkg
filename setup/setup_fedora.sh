#!/bin/bash
# Setup script for spkg: Fedora

sudo dnf install \
python3 \
python3-pip \
python3-requests \
python3-colorama \

sudo pip install \ # Not the best method
halo