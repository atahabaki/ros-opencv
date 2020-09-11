#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from mavros_msgs.msg import *
from mavros_msgs.srv import *

class EasyControl:
    def __init__(self):
        self.arming_srv_name = "/mavros/cmd/arming"
        self.takeoff_srv_name = "/mavros/cmd/takeoff"
        self.landing_srv_name = "/mavros/cmd/land"
        self.change_mode_srv_name = "/mavros/set_mode"
        self.tankmanager_change_pub = "tankmanager/status/change"

    def info(self,msg):
        rospy.loginfo(msg)

    def exc_occured(self, when="init", what="takeoff"):
        if when == "":
            print(f"Something happened while trying to {what}")
        else:
            print(f"Something happened while trying to {when} {what}")
    
    def wait4connection(self):
        self.info("Waiting 4 FCU connection...")
        while not rospy.is_shutdown():
            pass

    def __init_tankmanager_pub(self):
        self.tankmanager_pub = rospy.Publisher(self.tankmanager_change_pub,String,queue_size=10)

    def __publish_new_tank_stat(self,data="close",i=1):
        try:
            self.tankmanager_pub.publish(data)
        except:
            if i <= 5:
                self.exc_occured(what="publishing new servo status")
                time.sleep(1)
                i+=1
                self.__publish_new_tank_stat(data,i)
            else:
                self.exc_occured(what="tried 5 times... publishing new servo status")

    def opencover(self):
        self.__publish_new_tank_stat("open")

    def closecover(self):
        self.__publish_new_tank_stat("close")

    def __init_takeoff(self):
        rospy.wait_for_service(self.takeoff_srv_name)
        try:
            self.takeoff_clnt = rospy.ServiceProxy(self.takeoff_srv_name, CommandTOL)
        except rospy.ROSException:
            self.exc_occured()

    def takeoff(self,altitude):
        self.__init_takeoff()
        try:
            self.takeoff_clnt(altitude=altitude,latitude=0,longitude=0,min_pitch=0,yaw=0)
        except rospy.ROSException:
            self.exc_occured(when="")

    def __init_arming(self):
        rospy.wait_for_service(self.arming_srv_name)
        try:
            self.arming_clnt = rospy.ServiceProxy(self.arming_srv_name,CommandBool)
        except rospy.ROSException:
            self.exc_occured(what="arming")

    def arm(self):
        self.__init_arming()
        try:
            self.arming_clnt(True)
        except rospy.ROSException:
            self.exc_occured("","arming")

    def disarm(self):
        self.__init_arming()
        try:
            self.arming_clnt(False)
        except rospy.ROSException:
            self.exc_occured("","arming")

    def __init_landing(self):
        rospy.wait_for_service(self.landing_srv_name)
        try:
            self.landing_clnt = rospy.ServiceProxy(self.landing_srv_name,CommandTOL)
        except rospy.ROSException:
            self.exc_occured(what="landing")

    def land(self):
        self.__init_landing()
        try:
            self.landing_clnt(altitude=0,latitude=0,longitude=0,min_pitch=0,yaw=0)
        except rospy.ROSException:
            self.exc_occured(when="",what="landing")

    def __init_change_mode(self):
        rospy.wait_for_service(self.change_mode_srv_name)
        try:
            self.change_mode_clnt = rospy.ServiceProxy(self.change_mode_srv_name,SetMode)
        except:
            self.exc_occured(what="changing mode")

    def change_mode(self,mode_name="GUIDED"):
        self.__init_change_mode()
        try:
            self.change_mode_clnt(custom_mode=mode_name)
        except:
            self.exc_occured(when="",what="changing mode")
