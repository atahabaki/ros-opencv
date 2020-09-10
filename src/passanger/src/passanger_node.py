#!/usr/bin/env python
import rospy
from mavros_msgs.msg import WaypointReached
from passanger.srv import Reached, ReachedRequest, ReachedResponse

class Passanger:
    _NODE_NAME="passanger"
    _NODE_REACHED_SRV="passanger/reached"
    _NODE_REACHED_SBC="mavros/mission/reached"
    wp_number=None
    def __init__(self):
        rospy.init_node(self._NODE_NAME)

    def init_server(self):
        self.reach_srv = rospy.Service(self._NODE_REACHED_SRV,Reached,self.return_data)

    def init_subscriber(self):
        self.reach_sbc = rospy.Subscriber(self._NODE_REACHED_SBC,WaypointReached,self.get_data)

    def return_data(self,req):
        self.init_subscriber()
        rospy.wait_for_message(self._NODE_REACHED_SBC,WaypointReached)
        self.reach_sbc.unregister()
        print("Service")
        print(self.wp_number)
        return ReachedResponse(self.wp_number)
    
    def get_data(self,data):
        self.wp_number = data.wp_seq
        print("Subscriber")
        print(self.wp_number)

def main():
    passanger = Passanger()
    passanger.init_server()
    rospy.spin()

if __name__ == "__main__":
    try:
        main()
    except:
        print("Something happend")
