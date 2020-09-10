#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
from gpstracker.srv import Location, LocationRequest, LocationResponse

class GPSTracker:
    _NODE_NAME="gpstracker"
    _NODE_LOC_SRV="gpstracker/location"
    _NODE_LOC_SBC="mavros/global_position/global"
    latitude,longitude,altitude=None,None,None
    def __init__(self):
        rospy.init_node(self._NODE_NAME)

    def init_server(self):
        self.gpssrv = rospy.Service(self._NODE_LOC_SRV,Location,self.return_gps_data)

    def init_subscriber(self):
        self.gpssbc = rospy.Subscriber(self._NODE_LOC_SBC,NavSatFix,self.get_gps_data)

    def return_gps_data(self,req):
        self.init_subscriber()
        rospy.wait_for_message(self._NODE_LOC_SBC,NavSatFix)
        self.gpssbc.unregister()
        print("Service")
        print(self.latitude,self.longitude,self.altitude)
        return LocationResponse(self.latitude,self.longitude,self.altitude)
    
    def get_gps_data(self,data):
        self.latitude,self.longitude,self.altitude=data.latitude,data.longitude,data.altitude
        print("Subscriber")
        print(self.latitude,self.longitude,self.altitude)

def main():
    gpstracker = GPSTracker()
    gpstracker.init_server()
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except:
        print("Something happend...")
