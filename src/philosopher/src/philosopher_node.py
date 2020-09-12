#!/usr/bin/env python
import rospy
import time
from easyctrl import EasyControl
#from finder.msg import Where

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
    easyctrl = EasyControl()
    rospy.init_node("philosopher")
    while not rospy.is_shutdown():
        x = menu()
        if x == "1":
            easyctrl.arm()
        elif x == "2":
            easyctrl.disarm()
        elif x == "3":
            easyctrl.change2Guided()
        elif x == "4":
            easyctrl.change2Stabilize()
        elif x == "5":
            easyctrl.takeoff()
        elif x == "6":
            easyctrl.land()
        else:
            exit()

if __name__ == "__main__":
    try:
        main()
    except:
        rospy.logerr("Exception occured while main...")
