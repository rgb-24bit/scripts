#!/bin/bash
#
# VPN Server Usability Testing

SERVER_NAMES=""
SERVER_DOMAIN=""
COUNT=1
TIMEOUT=1

while getopts "c:t:" arg
do
    case $arg in
        c)
            COUNT=$OPTARG
            ;;
        t)
            TIMEOUT=$OPTARG
            ;;
        ?)
        ;;
    esac
done

for SERVER_NAME in $SERVER_NAMES
do
    SERVER=$SERVER_NAME.$SERVER_DOMAIN

    TEST=`ping -c $COUNT -t $TIMEOUT $SERVER | grep round-trip`

    if [ -z "$TEST" ]; then
        # Faild with red color
        echo -e "\033[31m $SERVER \033[0m"
    else
        echo -e "\033[32m $SERVER -> $TEST \033[0m"
    fi
done

