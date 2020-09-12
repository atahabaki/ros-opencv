#!/usr/bin/env python
import rospy
import time
from finder.srv import *
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

    def __arm(self,data=True):
        self.arming_clnt = rospy.ServiceProxy(self.arming_srv_name,CommandBool)
        self.arming_clnt(data)

    def arm(self):
        rospy.wait_for_service(self.arming_srv_name)
        try:
            self.__arm()
        except:
            rospy.logerr("Arming failed.")

    def disarm(self):
        rospy.wait_for_service(self.arming_srv_name)
        try:
            self.__arm(data=False)
        except:
            rospy.logerr("Disarming failed.")

    #######################################
    # Servo Ctrl
    #######################################

    def __pwm(self,data="open"):
        self.tankmanager_change_pub = rospy.Publisher(self.tankmanager_change_name, String, queue_size=10)
        self.tankmanager_change_pub.publish(data)

    def open_cover(self):
        rospy.wait_for_message(self.tankmanager_status_name,String)
        try:
            self.__pwm()
        except:
            rospy.logerr("Open cover failed.")

    def close_cover(self):
        rospy.wait_for_message(self.tankmanager_status_name,String)
        try:
            self.__pwm()
        except:
            rospy.logerr("Close cover failed.")

    #######################################
    # Mode changing
    #######################################

    def __mode(self,mode_name="GUIDED",base_mode=0):
        self.mavros_mode_clnt = rospy.ServiceProxy(self.change_mode_srv_name,SetMode)
        self.mavros_mode_clnt(base_mode=base_mode,custom_mode=mode_name)

    def change2Guided(self):
        rospy.wait_for_service(self.change_mode_srv_name)
        try:
            self.__mode()
        except:
            rospy.logerr("Set mode \"GUIDED\" failed.")

    def change2Stabilize(self):
        rospy.wait_for_service(self.change_mode_srv_name)
        try:
            self.__mode(mode_name="STABILIZE")
        except:
            rospy.logerr("Set mode \"STABILIZE\" failed.")

    
    #######################################
    # Landing Client
    #######################################
    
    def __land(self):
        self.landing_clnt = rospy.ServiceProxy(self.landing_srv_name,CommandTOL)
        self.landing_clnt(altitude=0,latitude=0,longtitude=0,min_pitch=0,yaw=0)

    def land(self):
        rospy.wait_for_service(self.landing_srv_name)
        try:
            self.__land()
        except:
            rospy.logerr("Landing failed.")

    #######################################
    # Takeoff Client
    #######################################
    
    def __takeoff(self,_altitude):
        self.landing_clnt = rospy.ServiceProxy(self.takeoff_srv_name,CommandTOL)
        self.landing_clnt(altitude=_altitude,latitude=0,longtitude=0,min_pitch=0,yaw=0)

    def takeoff(self,altitude=6):
        rospy.wait_for_service(self.landing_srv_name)
        try:
            self.__takeoff(_altitude=altitude)
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
