#!/usr/bin/env python
import rospy
import time
from finder.msg import Where
from std_msgs.msg import String
from mavros_msgs.msg import *
from mavros_msgs.srv import *

class FinderMonitor:
    _FINDER_WHERE="finder/where"
    def __init__(self):
        self.finder_sbc = rospy.Subscriber(self._FINDER_WHERE,Where,self.do)
        # Limit values
        self._OUT_LIMIT_INT=5000
        self._OUT_LIMIT_FLOAT=5000.0
        # Where object
        self.where=Where()
        self.where.cx = self._OUT_LIMIT_INT
        self.where.cy = self._OUT_LIMIT_INT
        self.where.distance = self._OUT_LIMIT_FLOAT
        self.where.distance_perc = self._OUT_LIMIT_FLOAT
        self.where.angle = self._OUT_LIMIT_FLOAT
        self.detected=False
    
    def _chng_cx(self,data):
        self.where.cx = data

    def _chng_cy(self,data):
        self.where.cy = data

    def _chng_dist(self,data):
        self.where.distance = data

    def _chng_perc(self,data):
        self.where.distance_perc = data

    def _chng_ang(self,data):
        self.where.angle = data

    def _is_detected(self,data):
        if data.cx == 5000 and data.cy == 5000:
            self.detected = False
        else:
            self.detected = True

    def change_where(self,data):
        self._chng_cx(data.cx)
        self._chng_cy(data.cy)
        self._chng_dist(data.distance)
        self._chng_perc(data.distance_perc)
        self._chng_ang(data.angle)
        self._is_detected(data)

    def do(self,data):
        self.change_where(data)
        return data

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
        # Should be in another Thread
        self.findermon = FinderMonitor()
        if self.findermon.detected:
            #do stuff...
            pass
        rospy.spin()

def main():
    philosopher = Philosopher()
    #if philosopher.findermon.changed:
    #    rospy.loginfo("Changed...")

if __name__=="__main__":
    try:
        main()
    except:
        pass
