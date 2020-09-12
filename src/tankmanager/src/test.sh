#!/usr/bin/env bash
while true
do
	rostopic pub -1 /tankmanager/status/change std_msgs/String "open"
	sleep 1
	rostopic pub -1 /tankmanager/status/change std_msgs/String "open"
	sleep 1
done
