#! /bin/bash

PKG=package

rm -rf "$PKG"
mkdir "$PKG"
pip install . --target "$PKG"

cd "$PKG"
zip -r9 ../labelbot.zip .
cd ..

rm -rf "$PKG"
