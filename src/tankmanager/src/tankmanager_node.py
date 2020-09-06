#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import String
import navio.pwm
import navio.util

class TankManager:
    _NODE_NAME="tankmanager"
    _NODE_STATUS="tankmanager/status"
    _NODE_CHANGE_STATUS="tankmanager/status/change"

    def __init__(self,rc_channel=4,min_pwm=1.250,max_pwm=1.750):
        self.rc_channel=rc_channel
        self.min_pwm=min_pwm
        self.max_pwm=max_pwm
        self._init_node()
        self._init_states()

    def _init_node(self):
        rospy.init_node(self._NODE_NAME)
        self.pub_stat = rospy.Publisher(self._NODE_STATUS, String, queue_size=30)
        self.sbc_stat = rospy.Subscriber(self._NODE_CHANGE_STATUS, String, self.change_next_state)
        self.rate = rospy.Rate(30)

    def _init_states(self):
        self.state = "close"
        self.next_state = "close"

    def change_next_state(self,data):
        self.next_state = data.data

    def change_state(self,state="open"):
        self.state = state

    def publish_status(self):
        self.pub_stat.publish(self.state)

    def send_min_pwm(self,pwm):
        rospy.loginfo("Sending min pwm ({}) to {}. channel...".format(self.min_pwm,self.rc_channel))
        pwm.set_duty_cycle(self.min_pwm)
        rospy.loginfo("Sent")
        self.sleep(1)

    def send_max_pwm(self,pwm):
        rospy.loginfo("Sending max pwm ({}) to {}. channel...".format(self.min_pwm,self.rc_channel))
        pwm.set_duty_cycle(self.max_pwm)
        rospy.loginfo("Sent")
        self.sleep(1)

    def _received_close(self,pwm):
        rospy.loginfo("RECEIVED close")
        self.change_state("close")
        self.send_max_pwm(pwm)

    def _received_open(self,pwm):
        rospy.loginfo("RECEIVED: open")
        self.change_state()
        self.send_min_pwm(pwm)

    def _still_open(self,pwm):
        rospy.loginfo("STILL open")
        self.send_min_pwm(pwm)

    def _still_close(self,pwm):
        rospy.loginfo("STILL close")
        self.send_min_pwm(pwm)

    def send_pwm_continuesly(self):
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.enable()
            pwm.set_period(50)
            while(True):
                if self.next_state==self.state:
                    if self.state=="open":
                        self._still_open(pwm)
                    elif self.state=="close":
                        self._still_close(pwm)
                    else:
                        rospy.logerr("Shit")
                else:
                    if self.next_state == "open":
                        self._received_open(pwm)
                    elif self.next_state == "close":
                        self._received_close(pwm)
                    else:
                        rospy.logerr("Ooo!")

    def task_failed(self):
        self.pub_stat.publish("failed")

    def sleep(self,sleep_time=5):
        i=0
        while(True):
            if i >= sleep_time:
                break
            time.sleep(1)
            i+=1
            rospy.loginfo("slept {} second(s)".format(i))

    def openAndClose(self,sleep_time=5):
        self.send_pwm_continuesly()

def main():
    tankmngr = TankManager(4)
    try:
        tankmngr.openAndClose(5)
    except:
        tankmngr.task_failed()
if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
