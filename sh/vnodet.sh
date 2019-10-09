#!/bin/bash
#
# VPN Server Usability Testing

SERVER_NAMES=""
SERVER_DOMAIN=""

for SERVER_NAME in $SERVER_NAMES
do
    SERVER=$SERVER_NAME.$SERVER_DOMAIN

    TEST=`ping -c 1 -t 1 $SERVER | grep round-trip`

    if [ -z "$TEST" ]; then
        echo -e "\033[31m $SERVER \033[0m"
    else
        echo -e "\033[32m $SERVER \033[0m"
    fi
done

