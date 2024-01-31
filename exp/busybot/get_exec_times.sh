#!/bin/bash

IFS=" " read -r -a completionTimes <<< "$(kubectl get -n busybot jobs --field-selector status.successful=1 -o jsonpath='{.items[*].status.completionTime}')"
IFS=" " read -r -a startTimes <<< "$(kubectl get -n busybot jobs --field-selector status.successful=1 -o jsonpath='{.items[*].status.startTime}')"

for i in "${!completionTimes[@]}"; do 
    startTime=$(date --date "${startTimes[$i]}" +%s)
    endTime=$(date --date "${completionTimes[$i]}" +%s)
    echo "$((endTime - startTime))"
done
