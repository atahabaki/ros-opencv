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
    def __init__(self,rc_channel=6,min_pwm=.750,max_pwm=1.350):
        self.status = False # Status => False =: Cover is already closed, True =: Cover is already open
        self.rc_channel=rc_channel
        self.min_pwm=min_pwm
        self.max_pwm=max_pwm
        #rospy.init_node(self._NODE_NAME,anonymous=True)
        rospy.init_node(self._NODE_NAME)
        self.pub_stat = rospy.Publisher(self._NODE_STATUS, String, queue_size=10)
        self.rate = rospy.Rate(60)
        #If apm is running kill this process
        navio.util.check_apm()

    def task_finished(self):
        self.pub_stat.publish("finished")
    
    def task_failed(self):
        self.pub_stat.publish("failed")

    def changeStatus(self,status=False):
        self.status=status

    def openCover(self):
        print("Opening")
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.set_period(50)
            pwm.enable()
            pwm.set_duty_cycle(self.max_pwm)
        print("Opened")
        self.changeStatus(status=True)

    def closeCover(self):
        print("Closing")
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.set_period(50)
            pwm.enable()
            pwm.set_duty_cycle(self.min_pwm)
        print("Closed")
        self.changeStatus()

    def openAndClose(self,sleep_time=5):
        self.openCover()
        self.changeStatus(status=True)
        time.sleep(sleep_time)
        self.closeCover()
        self.changeStatus()

    def toggle_cover(self):
        if self.status == True:
            self.closeCover()
        else:
            self.openCover()

def main():
    tankmngr = TankManager()
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
