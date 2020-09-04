#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
from tankmanager.srv import ToggleCover, ToggleCoverRequest, ToggleCoverResponse
import navio.pwm
import navio.util

class TankManager:
    _NODE_NAME="tankmanager"
    _NODE_STATUS="tankmanager/status"
    def __init__(self,rc_channel=4,min_pwm=1.250,max_pwm=1.750):
        self.rc_channel=rc_channel
        self.min_pwm=min_pwm
        self.max_pwm=max_pwm
        #rospy.init_node(self._NODE_NAME,anonymous=True)
        rospy.init_node(self._NODE_NAME)
        self.pub_stat = rospy.Publisher(self._NODE_STATUS, String, queue_size=10)
        self.rate = rospy.Rate(60)
        #If apm is running kill this process

    def task_finished(self):
        self.pub_stat.publish("finished")
    
    def task_failed(self):
        self.pub_stat.publish("failed")

    def openCover(self,atime=1):
        rospy.loginfo("opening cover")
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.set_period(50)
            pwm.enable()
            start=time.time()
            while(True):
                now=time.time()
                dist=now-start
                if dist >= atime:
                    break
                pwm.set_duty_cycle(self.max_pwm)

    def closeCover(self,atime=1):
        rospy.loginfo("closing cover")
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.set_period(50)
            pwm.enable()
            start=time.time()
            while(True):
                now=time.time()
                dist=now-start
                if dist >= atime:
                    break
                pwm.set_duty_cycle(self.min_pwm)

    def sleep(self,sleep_time=5):
        i=0
        while(True):
            if i >= sleep_time:
                break
            time.sleep(1)
            i+=1
            rospy.loginfo("slept {} second(s)".format(i))

    def openAndClose(self,sleep_time=5):
        self.openCover()
        self.sleep()
        self.closeCover()

    def closeAndOpen(self,sleep_time=5):
        self.closeCover()
        self.sleep()
        self.openCover()

def main():
    tankmngr = TankManager(4)
    try:
        tankmngr.openAndClose(5)
    except:
        tankmngr.task_failed()
    tankmngr.task_finished()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
