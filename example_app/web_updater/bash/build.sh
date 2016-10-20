#!/bin/bash
cd .buildozer/android/app/
zip ../../../$1 *
cd ../../../
mv $1 $2
