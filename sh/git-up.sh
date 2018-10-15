#!/bin/bash
#
# Fetch upstream and merge to local branch.

upstream=`git remote | grep upstream`

if [ ! -n "$upstream" ]; then
    echo "Not found remote named upstream."
else
    if [ ! -n "$1" ]; then
        echo "Usage: git up <branch>"
    else
        git fetch upstream
        git merge upstream/$1
    fi
fi

