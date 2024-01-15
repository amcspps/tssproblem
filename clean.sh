#!/bin/bash

if [ "$1" == "test/" ]; then
    rm -rf test/res_gen/output/*
    rm -rf test/res_gen/additional/*
    rm -rf test/res_cmaes/output/*
    rm -rf test/res_cmaes/additional/*
    rm -rf test/res_pso/output/*
    rm -rf test/res_pso/additional/*
    echo "Ok test"
elif [ "$1" == "medium/" ]; then
    rm -rf medium/res_gen/output/*
    rm -rf medium/res_gen/additional/*
    rm -rf medium/res_cmaes/output/*
    rm -rf medium/res_cmaes/additional/*
    rm -rf medium/res_pso/output/*
    rm -rf medium/res_pso/additional/*
    rm -rf medium/res_gen/results/*
    rm -rf medium/res_pso/results/*
    rm -rf medium/res_cmaes/results/*

    echo "Ok medium"
elif [ "$1" == "large/" ]; then
    rm -rf large/$1/output/*
    rm -rf large/$1/additional/*
    echo "Ok large"
elif [ "$1" == "all" ]; then
    rm -rf all/$1/output/*
    rm -rf all/$1/additional/*
    rm -rf medium/$1/output/*
    rm -rf medium/$1/additional/*
    rm -rf test/$1/output/*
    rm -rf test/$1/additional/*
    echo "Ok all"
else
    echo "Invalid argument. Usage: $0 <test/|medium/|large/|all>"
fi
