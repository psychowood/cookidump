#!/bin/sh

COMMAND=./cookidump.py

if [ "$#" -eq 0 ]
then
  python3 $COMMAND -h
  exit 0
fi

python3 $COMMAND $*