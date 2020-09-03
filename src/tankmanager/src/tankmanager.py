#!/usr/bin/env python3
import rospy
import time
from std_msgs.msg import String
import navio.pwm
import navio.util

class TankManager:
    def __init__(self,rc_channel=6,min_pwm=.750,max_pwm=1.350):
        self.rc_channel=rc_channel
        self.min_pwm=min_pwm
        self.max_pwm=max_pwm
        rospy.init_node("tankmanager",anonymous=True)
        self.pub_stat = rospy.Publisher("tankmanager/status", String, queue_size=10)
        self.rate = rospy.Rate(1)

    def task_finished(self):
        self.pub_stat.publish("finished")
    
    def task_failed(self):
        self.pub_stat.publish("failed")

    def openCover(self):
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.set_period(50)
            pwm.enable()
            pwm.set_duty_cycle(self.max_pwm)

    def closeCover(self):
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.set_period(50)
            pwm.enable()
            pwm.set_duty_cycle(self.min_pwm)

    def openAndClose(self,sleep_time=5):
        self.openCover()
        time.sleep(sleep_time)
        self.closeCover()

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
