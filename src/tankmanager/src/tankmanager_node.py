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

    def __init__(self,rc_channel=9,min_pwm=.800,max_pwm=2.200):
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

    def send_pwm_continuesly(self):
        with navio.pwm.PWM(self.rc_channel) as pwm:
            pwm.enable()
            pwm.set_period(50)

            def _max_pwm():
                pwm.set_duty_cycle(self.max_pwm)

            def send_max_pwm():
                rospy.loginfo("Sending max pwm ({}) to {}. channel...".format(self.min_pwm,self.rc_channel))
                try:
                    _max_pwm()
                except:
                    rospy.logerr("Error occured while sending max pwm...")
                rospy.loginfo("Sent")
                self.pub_stat.publish("open")

            def _min_pwm():
                pwm.set_duty_cycle(self.min_pwm)

            def send_min_pwm():
                rospy.loginfo("Sending max pwm ({}) to {}. channel...".format(self.min_pwm,self.rc_channel))
                try:
                    _min_pwm()
                except:
                    rospy.logerr("Error occured while sending min pwm...")
                rospy.loginfo("Sent")
                self.pub_stat.publish("close")

            while(True):
                if self.next_state==self.state:
                    if self.state=="open":
                        rospy.loginfo("STILL open")
                        send_min_pwm()
                    elif self.state=="close":
                        rospy.loginfo("STILL close")
                        send_max_pwm()
                    else:
                        rospy.logerr("States are the same but... unknown error happend...")
                else:
                    if self.next_state == "open":
                        rospy.loginfo("RECEIVED open")
                        send_min_pwm()
                        self.change_state("open")
                    elif self.next_state == "close":
                        rospy.loginfo("RECEIVED close")
                        send_max_pwm()
                        self.change_state("close")
                    else:
                        rospy.logerr("Ooo!")
            self.sleep(1)
        rospy.spin()
            
    def test_node(self):
        while(True):
            if self.next_state==self.state:
                if self.state=="open":
                    rospy.loginfo("STILL open")
                elif self.state=="close":
                    rospy.loginfo("STILL close")
                else:
                    rospy.logerr("States are the same but... unknown error happend...")
            else:
                if self.next_state == "open":
                    rospy.loginfo("RECEIVED open")
                    self.change_state("open")
                elif self.next_state == "close":
                    rospy.loginfo("RECEIVED close")
                    self.change_state("close")
                else:
                    rospy.logerr("Ooo!")
        self.sleep(1)

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

def main():
    tankmngr = TankManager(9)
    try:
        tankmngr.send_pwm_continuesly()
        #tankmngr.test_node()
    except:
        tankmngr.task_failed()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
        #print("Something happend")
