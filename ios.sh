#!/bin/sh
IFS=$'\n'
my_array=( $( instruments -s devices | grep "iPhone" | tr "\n" ", " | sed 's/,$/ /' | tr " " "\n") )
echo ${my_array[*]}


