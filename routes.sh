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

cd "$folder_name/od2trips"
od2trips -c od2trips.config.xml -n from_to.taz.xml -o trips.odtrips.xml
cd ../duaIterate/iterations
rm -rf *
python /usr/share/sumo/tools/assign/duaIterate.py \
 -n /home/pavel/dev/diplom/tssproblem/$folder_name/net/osm.net.xml \
 -t /home/pavel/dev/diplom/tssproblem/$folder_name/od2trips/trips.odtrips.xml 