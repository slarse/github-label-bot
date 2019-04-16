#! /bin/bash

PKG=package

rm -rf "$PKG"
mkdir "$PKG"
python3 -m pip install . --target "$PKG"

cd "$PKG"
zip -r9 ../labelbot.zip .
cd ..

rm -rf "$PKG"
