#!/bin/bash
cd "$(dirname "$0")"
i='1'
while true;
do
  bash clean-active.sh > /dev/null 2>&1
  sleep 60
done
