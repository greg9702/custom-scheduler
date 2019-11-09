#!/bin/bash

while [ 0 ]
do
    date '+%Y-%m-%d %H:%M:%S'
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | sed '1d' | cut -d/ -f1 | awk '{print $1" "$3}'
done
