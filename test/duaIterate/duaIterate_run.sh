#!/bin/bash
if [ -d "iterations" ]; then
    cd iterations
else
    mkdir "iterations"
    cd iterations
fi


python /usr/share/sumo/tools/assign/duaIterate.py -n /home/pavel/dev/diplom/tssproblem/test/net/straight_cross.net.xml -t /home/pavel/dev/diplom/tssproblem/test/od2trips/trips.odtrips.xml