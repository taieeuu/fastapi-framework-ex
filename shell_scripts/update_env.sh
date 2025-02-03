#!/bin/bash

if [ -z "$1" ]; then
  echo "請提供環境參數"
  echo "用法: $0 <env>"
  exit 1
fi

if [ "$1" = "prod" ]; then
  IP_ADDRESS="172.22.1.150"
elif [ "$1" = "prod2" ]; then
  IP_ADDRESS="172.22.1.151"
elif [ "$1" = "uat" ]; then
  IP_ADDRESS="172.22.2.150"
else
  echo "環境參數只能是 prod 或 prod2 或 uat"
  exit 1
fi

scp ./shell_scripts/$1.env ap@$IP_ADDRESS:/home/ap/.env
