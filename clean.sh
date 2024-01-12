#!/bin/bash

if [ "$1" == "test/" ]; then
    rm -rf test/output/*
    rm -rf test/additional/*
    echo "Ok test"
elif [ "$1" == "medium/" ]; then
    rm -rf medium/output/*
    rm -rf medium/additional/*
    echo "Ok medium"
elif [ "$1" == "large/" ]; then
    rm -rf large/output/*
    rm -rf large/additional/*
    echo "Ok large"
elif [ "$1" == "all" ]; then
    rm -rf all/output/*
    rm -rf all/additional/*
    rm -rf medium/output/*
    rm -rf medium/additional/*
    rm -rf test/output/*
    rm -rf test/additional/*
    echo "Ok all"
else
    echo "Invalid argument. Usage: $0 <test/|medium/|large/|all>"
fi
