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

    #######################################
    # State managing
    #######################################

    #######################################
    # Drone Control
    #######################################

