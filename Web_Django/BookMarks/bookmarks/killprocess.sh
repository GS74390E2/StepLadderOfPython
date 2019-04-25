#!/bin/sh
set -u
set -x

port=$1
pids=`ps -ef | grep $port | grep "python manage.py" | awk '{print $2}'`
for pid in $pids
do
	kill -9 $pid
done
