#!/bin/bash
mkdir "$HOME/Desktop/temporary_apupdater_folder1111"
mv bin "$HOME/Desktop/temporary_apupdater_folder1111/"
mv .buildozer "$HOME/Desktop/temporary_apupdater_folder1111/"
zip "$1" *
mv "$HOME/Desktop/temporary_apupdater_folder1111/*" "$PWD/"
rm -r "$HOME/Desktop/temporary_apupdater_folder1111"
mv "$1" "$2"
