#!/usr/bin/env python
import rospy
import time
from finder.msg import Where
from std_msgs.msg import String
from mavros_msgs.msg import *
from mavros_msgs.srv import *

class TankController:
    _TANKMNGR_CHANGE="tankmanager/status/change"
    def __init__(self):
        self.pub_stat_ = rospy.Publisher(self._TANKMNGR_CHANGE,String,queue_size=30)
    
    def publishThis(self,data,i=1):
        try:
            self.pub_stat_.publish(data)
        except:
            if i <= 5:
                print("Unknown error occured while publishing \"{}\" on this topic: {}".format(data,self._TANKMNGR_CHANGE))
                time.sleep(1)
                i+=1
                self.publishThis(data,i)
            else:
                print("Tried 5 times... Nothing works... Try to debug the code... Or look at the log files...")
                exit()

class WaypointManager:
    def __init__(self):
        self.waypoints=[]
        # TODO create a /mavros/mission/push client
    
    def newWaypoint(self,cmd,xlat,ylong,zalt,cur,cont,params=(0,0,0,0)):
        wp = Waypoint()
        wp.frame=0 # 0...5
        wp.command=cmd # Command Number
        wp.is_current=cur # bool 
        wp.autocontinue=cont # bool
        wp.param1=params[0]
        wp.param2=params[1]
        wp.param3=params[2]
        wp.param4=params[3]
        wp.x_lat=xlat
        wp.y_long=ylong
        wp.z_alt=zalt
        return wp

class Philosopher:
    _NODE_NAME="philosopher"
    def __init__(self):
        # TODO init FinderMonitor, TankController, WaypointManager
        rospy.init_node(self._NODE_NAME)
        self.tankmngr = TankController()

    def close_cover(self):
        self.tankmngr.publishThis("close")

    def open_cover(self):
        self.tankmngr.publishThis("open")

def main():
    philosopher = Philosopher()
    #if philosopher.findermon.changed:
    #    rospy.loginfo("Changed...")

if __name__=="__main__":
    try:
        main()
    except:
        pass
