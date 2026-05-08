#!/bin/bash

while true
do
    echo "stop pressing brakes"
    cansend fordka 165#10c0000000000000

    echo "run"
    cansend fordka 167#727FFF00001A0000
    sleep 3

    echo "turn right"
    cansend fordka 07e#7edeadbeef
    sleep 3

    echo "turn left"
    cansend fordka 07e#82deadbeef
    sleep 3

    echo "straight"
    cansend fordka 07e#80deadbeef
    sleep 3

    echo "stop"
    cansend fordka 165#20c0000000000000
    sleep 3
done
