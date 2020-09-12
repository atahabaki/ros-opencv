#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from finder.srv import *
from mavros_msgs.msg import *
from mavros_msgs.srv import *

class EasyControl:
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

