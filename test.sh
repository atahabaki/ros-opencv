#!/usr/bin/env bash
rosservice call /mavros/set_mode "base_mode: 0  
custom_mode: 'GUIDED'"  
rosservice call /mavros/cmd/arming "value: true"
rosservice call /mavros/cmd/takeoff "{min_pitch: 0.0, yaw: 0.0, latitude: 0.0, longitude: 0.0, altitude: 10.0}" 
sleep 3
rosservice call /mavros/set_mode "base_mode: 0  
custom_mode: 'AUTO'"  
while true; do
	rostopic echo -n1 /mavros/mission/waypoints
	rosservice call /mavros/mission/pull
done
