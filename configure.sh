#!/bin/bash

echo -e "This script is only intended to use with spkg-compose"
echo -e "Exit NOW if you are running this script outside of spkg-compose"
sleep 3
mkdir _work
mkdir -p _work/usr/bin
cp target/release/spkg _work/usr/bin
cp -r data/var _work/
cp -r data/etc _work/