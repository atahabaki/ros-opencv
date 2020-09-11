#!/usr/bin/env python
import rospy
import time
from easyctrl import EasyControl
#from finder.msg import Where

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
        #self.tankmngr = TankController()

easyctrl = EasyControl()
def test():
    while(True):
        print("""
1) Arm
2) Disarm
3) Change mode to Stabilize
4) Change mode to Guided
5) Takeoff
6) Land
7) Open cover
8) Close cover
9) Open cover when detected red...
        """)
        op = input("Command: ")
        op = op.strip()
        try:
            op = int(op)
        except:
            print("Wrong type of command...")
        if op==1:
            easyctrl.arm()
        elif op==2:
            easyctrl.disarm()
        elif op==3:
            easyctrl.change_mode("STABILIZE")
        elif op==4:
            easyctrl.change_mode()
        elif op==5:
            easyctrl.takeoff()
        elif op==6:
            easyctrl.land()
        elif op==7:
            easyctrl.opencover()
        elif op==8:
            easyctrl.closecover()
        elif op==9:
            resp=easyctrl.findobj()
            #print(resp)
            if resp.cx!=None and resp.cx!=5000 and resp.cy!=None and resp.cy!=5000:
                print("Found")
            else:
                print("Not found")
               #easyctrl.opencover()
        else:
            easyctrl.exc_occured("finding corresponding operation","input")

def main():
    pass

if __name__=="__main__":
    try:
        test()
    except:
        pass
