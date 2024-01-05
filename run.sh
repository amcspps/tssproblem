#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <folder_name>"
    exit 1
fi

folder_name="$1"

if [ ! -d "$folder_name" ]; then
    echo "Error: Folder '$folder_name' not found."
    exit 1
fi

pwd

cd "$folder_name/od2trips" || exit 1

./od2trips_run.sh

cd ".."

cd "duaIterate" || exit 1

./clean.sh
./duaIterate_run.sh

cd -
