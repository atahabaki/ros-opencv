#!/usr/bin/env python
import rospy
import time
from finder.srv import *
from std_msgs import String
from mavros_msgs.msg import *
from mavros_msgs.srv import *
#from philosopher import EasyControl
#from finder.msg import Where

class Philosopher:
    def __init__(self):
        self._INT_LIMIT=5000
        self._FLOAT_LIMIT=5000
        self.arming_srv_name = "/mavros/cmd/arming"
        self.takeoff_srv_name = "/mavros/cmd/takeoff"
        self.landing_srv_name = "/mavros/cmd/land"
        self.change_mode_srv_name = "/mavros/set_mode"
        self.tankmanager_change_name = "tankmanager/status/change"
        self.tankmanager_status_name = "tankmanager/status"
        self.finder_srv_name = "/finder/where"
        self.mavros_state_name = "/mavros/state"

    def init(self):
        rospy.init_node("philosopher")

    #######################################
    # Arming
    #######################################

    def arm(self):
        rospy.wait_for_service(self.arming_srv_name)
        try:
            arming_clnt = rospy.ServiceProxy(self.arming_srv_name,CommandBool)
            arming_clnt(True)
        except:
            rospy.logerr("Arming failed.")

    def disarm(self):
        rospy.wait_for_service(self.arming_srv_name)
        try:
            arming_clnt = rospy.ServiceProxy(self.arming_srv_name,CommandBool)
            arming_clnt(False)
        except:
            rospy.logerr("Disarming failed.")

    #######################################
    # Servo Ctrl
    #######################################

    def open_cover(self):
        rospy.wait_for_message(self.tankmanager_status_name,String)
        try:
            tankmanager_change_pub = rospy.Publisher(self.tankmanager_change_name, String, queue_size=10)
            tankmanager_change_pub.publish("open")
        except:
            rospy.logerr("Open cover failed.")

    def close_cover(self):
        rospy.wait_for_message(self.tankmanager_status_name,String)
        try:
            tankmanager_change_pub = rospy.Publisher(self.tankmanager_change_name, String, queue_size=10)
            tankmanager_change_pub.publish("close")
        except:
            rospy.logerr("Close cover failed.")

    #######################################
    # Mode changing
    #######################################

    def change2Guided(self):
        rospy.wait_for_service(self.change_mode_srv_name)
        try:
            self.mavros_mode_clnt = rospy.ServiceProxy(self.change_mode_srv_name,SetMode)
            self.mavros_mode_clnt(custom_mode="GUIDED")
        except:
            rospy.logerr("Set mode \"GUIDED\" failed.")

    def change2Stabilize(self):
        rospy.wait_for_service(self.change_mode_srv_name)
        try:
            self.mavros_mode_clnt = rospy.ServiceProxy(self.change_mode_srv_name,SetMode)
            self.mavros_mode_clnt(custom_mode="STABILIZE")
        except:
            rospy.logerr("Set mode \"STABILIZE\" failed.")

    
    #######################################
    # Landing Client
    #######################################

    def land(self):
        rospy.wait_for_service(self.landing_srv_name)
        try:
            self.landing_clnt = rospy.ServiceProxy(self.landing_srv_name,CommandTOL)
            self.landing_clnt(altitude=0,latitude=0,longtitude=0,min_pitch=0,yaw=0)
        except:
            rospy.logerr("Landing failed.")

    #######################################
    # Takeoff Client
    #######################################
    
    def takeoff(self,_altitude=6):
        rospy.wait_for_service(self.landing_srv_name)
        try:
            self.landing_clnt = rospy.ServiceProxy(self.takeoff_srv_name,CommandTOL)
            self.landing_clnt(altitude=_altitude,latitude=0,longtitude=0,min_pitch=0,yaw=0)
        except:
            rospy.logerr("Takeoff failed.")

    #######################################
    # State Tests
    #######################################

    #######################################
    # Drone Control
    #######################################

def menu():
    print("""
1) Arm
2) Disarm
3) Change mode to GUIDED
4) Change mode to STABILIZE
5) Takeoff
6) Land
""")
    x = input("Command (1-6): ")
    x = x.strip()
    return x

def main():
    philosopher = Philosopher()
    while not rospy.is_shutdown():
        x = menu()
        if x == "1":
            philosopher.arm()
        elif x == "2":
            philosopher.disarm()
        elif x == "3":
            philosopher.change2Guided()
        elif x == "4":
            philosopher.change2Stabilize()
        elif x == "5":
            philosopher.takeoff()
        elif x == "6":
            philosopher.land()
        else:
            exit()

if __name__ == "__main__":
    try:
        main()
    except:
        rospy.logerr("Exception occured while main...")
