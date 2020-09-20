#!/usr/bin/env python
import math
import time
import rospy
from finder.srv import *
from nav_msgs.msg import *
from nav_msgs.srv import *
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from geometry_msgs.msg import *
from std_msgs.msg import String
#from philosopher import EasyControl
#from finder.msg import Where

class Philosopher:
    def __init__(self):
        self._INT_LIMIT=5000
        self._FLOAT_LIMIT=5000
        self.arming_srv_name = "/mavros/cmd/arming"
        self.takeoff_srv_name = "/mavros/cmd/takeoff"
        self.landing_srv_name = "/mavros/cmd/land"
        self.change_mode_srv_name = "/mavros/set_mode"
        self.tankmanager_change_name = "tankmanager/status/change"
        self.tankmanager_status_name = "tankmanager/status"
        self.finder_srv_name = "/finder/where"
        self.mavros_state_name = "/mavros/state"
        self.global_local_pos_name = "/mavros/global_position/local"
        self.setpos_local_name = "/mavros/setpoint_position/local"
        self.local_offset=0
        self.current_heading=0
        self.correction_heading=0
        self.local_desired_heading=0
        # To control servo, need a publisher
        self.__init_servo_pub()
        # Init all publisher and subscribers and variables...
        self.init_pub_sub()

    def init(self):
        rospy.init_node("philosopher")

    def __calc_psi(self,q0,q1,q2,q3):
        return math.atan2((2*(q0*q3+q1*q2)),(1-2*(math.pow(q2,2)+math.pow(q3,2))))

    #######################################
    # Arming
    #######################################

    def arm(self):
        self.set_destination(0,0,0,0)
        for _ in range(0,100):
            self.local_pos_pub.publish(self.waypoint)
            time.sleep(.1)
        rospy.loginfo("Arming drone")
        rospy.wait_for_service(self.arming_srv_name)
        try:
            arming_clnt = rospy.ServiceProxy(self.arming_srv_name,CommandBool)
            arming_clnt(True)
        except:
            rospy.logerr("Arming failed.")

    def disarm(self):
        rospy.wait_for_service(self.arming_srv_name)
        try:
            arming_clnt = rospy.ServiceProxy(self.arming_srv_name,CommandBool)
            arming_clnt(False)
        except:
            rospy.logerr("Disarming failed.")

    #######################################
    # Servo Ctrl
    #######################################
    
    def __init_servo_pub(self):
        self.tankmanager_change_pub = rospy.Publisher(self.tankmanager_change_name, String, queue_size=10)

    def open_cover(self):
        rospy.wait_for_message(self.tankmanager_status_name,String)
        try:
            self.tankmanager_change_pub.publish("open")
        except:
            rospy.logerr("Open cover failed.")

    def close_cover(self):
        rospy.wait_for_message(self.tankmanager_status_name,String)
        try:
            self.tankmanager_change_pub.publish("close")
        except:
            rospy.logerr("Close cover failed.")

    #######################################
    # Mode changing
    #######################################

    def change2Guided(self):
        rospy.wait_for_service(self.change_mode_srv_name)
        try:
            self.mavros_mode_clnt = rospy.ServiceProxy(self.change_mode_srv_name,SetMode)
            self.mavros_mode_clnt(custom_mode="GUIDED")
        except:
            rospy.logerr("Set mode \"GUIDED\" failed.")

    def change2Stabilize(self):
        rospy.wait_for_service(self.change_mode_srv_name)
        try:
            self.mavros_mode_clnt = rospy.ServiceProxy(self.change_mode_srv_name,SetMode)
            self.mavros_mode_clnt(custom_mode="STABILIZE")
        except:
            rospy.logerr("Set mode \"STABILIZE\" failed.")

    
    #######################################
    # Landing Client
    #######################################

    def land(self):
        rospy.wait_for_service(self.landing_srv_name)
        try:
            self.landing_clnt = rospy.ServiceProxy(self.landing_srv_name,CommandTOL)
            self.landing_clnt(altitude=0,latitude=0,longtitude=0,min_pitch=0,yaw=0)
        except:
            rospy.logerr("Landing failed.")

    #######################################
    # Takeoff Client
    #######################################
    
    def takeoff(self,_altitude=6):
        self.set_destination(0,0,_altitude,0)
        for _ in range(0,100):
            self.local_pos_pub.publish(self.waypoint)
            time.sleep(.1)
        rospy.wait_for_service(self.takeoff_srv_name)
        try:
            self.takeoff_clnt = rospy.ServiceProxy(self.takeoff_srv_name,CommandTOL)
            self.takeoff_clnt(altitude=_altitude,latitude=0,longtitude=0,min_pitch=0,yaw=0)
        except:
            rospy.logerr("Takeoff failed.")

    #######################################
    # State Tests
    #######################################

    #######################################
    # Drone Control
    #######################################

    def init_pub_sub(self):
        self.local_pos_pub = rospy.Publisher(self.setpos_local_name, PoseStamped, queue_size=10)
        self.global_local_sub = rospy.Subscriber(self.global_local_pos_name, Odometry, self.pose_cb)
        self.state_sub = rospy.Subscriber(self.mavros_state_name,State,self.state_cb)
        self.local_offset_pose = Point()
        self.current_pose = Odometry()
        self.current_pose_local = Point()
        self.waypoint = PoseStamped()
        self.correction_vector = Pose()

    def state_cb(self,data):
        self.current_state = data

    def init_local_frame(self):
        self.local_offset=0
        for _ in range(1,30+1):
            q0,q1=self.current_pose.pose.pose.orientation.w,self.current_pose.pose.pose.orientation.x
            q2,q3=self.current_pose.pose.pose.orientation.y,self.current_pose.pose.pose.orientation.z
            psi=self.__calc_psi(q0,q1,q2,q3)
            self.local_offset += psi*(180/math.pi)
            self.local_offset_pose.x = self.local_offset_pose.x+self.current_pose.pose.pose.position.x
            self.local_offset_pose.y = self.local_offset_pose.y+self.current_pose.pose.pose.position.y
            self.local_offset_pose.z = self.local_offset_pose.z+self.current_pose.pose.pose.position.z
        self.local_offset_pose.x /= 30
        self.local_offset_pose.y /= 30
        self.local_offset_pose.z /= 30
        self.local_offset /= 30
        rospy.loginfo("Coordinate offset set")
        rospy.loginfo("X axis is facing {}".format(self.local_offset))

    def pose_cb(self,data):
        self.current_pose = data
        self.enu2local(self.current_pose)
        q0,q1=self.current_pose.pose.pose.orientation.w,self.current_pose.pose.pose.orientation.x
        q2,q3=self.current_pose.pose.pose.orientation.y,self.current_pose.pose.pose.orientation.z
        psi=self.__calc_psi(q0,q1,q2,q3)
        self.current_heading = psi*(180/math.pi) - self.local_offset

    def set_heading(self, heading):
        self.local_desired_heading = heading
        heading = heading + self.correction_heading + self.local_offset

        rospy.loginfo("Desired heading {}".format(self.local_desired_heading))

        yaw,pitch,roll=heading*(math.pi/180),0,0

        cy,sy=math.cos(yaw*.5),math.sin(yaw*.5)
        cr,sr=math.cos(roll*.5),math.sin(roll*.5)
        cp,sp=math.cos(pitch*.5),math.sin(pitch*.5)

        self.waypoint.pose.orientation.w = cy * cr * cp + sy * sr * sp
        self.waypoint.pose.orientation.x = cy * sr * cp - sy * cr * sp
        self.waypoint.pose.orientation.y = cy * cr * sp + sy * sr * cp
        self.waypoint.pose.orientation.z = sy * cr * cp - cy * sr * sp
    
    def set_destination(self,x,y,z,psi):
        self.set_heading(psi)
        deg2grad = math.pi/180
        _param=self.correction_heading+self.local_offset-90
        Xlocal=x*math.cos(_param*deg2grad) - y*math.sin(_param*deg2grad)
        Ylocal=x*math.sin(_param*deg2grad) + y*math.cos(_param*deg2grad)
        Zlocal=z

        _x = Xlocal + self.correction_vector.position.x + self.local_offset_pose.x
        _y = Ylocal + self.correction_vector.position.y + self.local_offset_pose.y
        _z = Zlocal + self.correction_vector.position.z + self.local_offset_pose.z

        rospy.loginfo("Destination set to ({},{},{})".format(_x,_y,_z))

        self.waypoint.pose.position.x = _x
        self.waypoint.pose.position.y = _y
        self.waypoint.pose.position.z = _z

        self.local_pos_pub.publish(self.waypoint)

    def enu2local(self,curr_pos_enu=Odometry()):
        x = curr_pos_enu.pose.pose.position.x
        y = curr_pos_enu.pose.pose.position.y
        z = curr_pos_enu.pose.pose.position.z
        deg2grad=math.pi/180
        current_pos_local = Point()
        _param = self.local_offset - 90
        current_pos_local.x = x*math.cos(_param*deg2grad) - y*math.sin(_param*deg2grad)
        current_pos_local.y = x*math.sin(_param*deg2grad) + y*math.cos(_param*deg2grad)
        current_pos_local.z = z
        return current_pos_local

    def get_current_location(self):
        self.current_pose_local = self.enu2local()
        return self.current_pose_local

    def get_current_heading(self):
        return self.current_heading

    def wait4connect(self):
        rospy.loginfo("Connecting 2 FCU")
        while not self.current_state.connected:
            time.sleep(.1)
        if self.current_state.connected:
            rospy.loginfo("Connected 2 FCU")
        else:
            rospy.loginfo("Trouble connecting 2 FCU...")

    def wait4start(self):
        rospy.loginfo("Waiting user to set the mode to guided...")
        while not self.current_state.mode != "GUIDED":
            time.sleep(.1)
        if self.current_state.mode == "GUIDED":
            rospy.loginfo("Mode changed 2 GUIDED...")
        else:
            rospy.loginfo("Mode is not GUIDED...")

    def check_waypoint_reached(self,pos_tolerance=0.3,heading_tolerance=0.01):
        self.local_pos_pub.publish(self.waypoint)
        deltaX=abs(self.waypoint.pose.position.x - self.current_pose.pose.pose.position.x)
        deltaY=abs(self.waypoint.pose.position.y - self.current_pose.pose.pose.position.y)
        deltaZ=0
        dMag=math.sqrt(math.pow(deltaX,2)+math.pow(deltaY,2)+math.pow(deltaZ,2))
        rospy.loginfo("dMag {}".format(dMag))
        rospy.loginfo("Current pose ({},{},{})".format(self.current_pose.pose.pose.position.x,self.current_pose.pose.pose.position.y,self.current_pose.pose.pose.position.z))
        rospy.loginfo("Waypoint pose ({},{},{})".format(self.waypoint.pose.position.x,self.waypoint.pose.position.y,self.waypoint.pose.position.z))
        deg2grad=math.pi/180
        cosErr=math.cos(self.current_heading*deg2grad) - math.cos(self.local_desired_heading*deg2grad)
        sinErr=math.sin(self.current_heading*deg2grad) - math.sin(self.local_desired_heading*deg2grad)
        headingErr=math.sqrt(math.pow(cosErr,2)+math.pow(sinErr,2))
        if dMag < pos_tolerance and  headingErr < heading_tolerance:
            return True
        else:
            return False

def menu():
    print("""
1) Arm
2) Disarm
3) Change mode to GUIDED
4) Change mode to STABILIZE
5) Takeoff
6) Land
7) Open cover
8) Close cover
9) Try mission
10) The mission
""")
    x = input("Command (1-6): ")
    x = int(x)
    return x

class WaypointX:
    def __init__(self,x=0,y=0,z=0,psi=0):
        self.x=x
        self.y=y
        self.z=z
        self.psi=psi

def main():
    philosopher = Philosopher()
    philosopher.init()
    while not rospy.is_shutdown():
        x = menu()
        if x == 1:
            philosopher.arm()
        elif x == 2:
            philosopher.disarm()
        elif x == 3:
            philosopher.change2Guided()
        elif x == 4:
            philosopher.change2Stabilize()
        elif x == 5:
            philosopher.takeoff()
        elif x == 6:
            philosopher.land()
        elif x == 7:
            philosopher.open_cover()
        elif x == 8:
            philosopher.close_cover()
        elif x == 9:
            wplist=[WaypointX(0,0,6,0),WaypointX(20,0,6,0)]
            i=0
            print("len",len(wplist))
            philosopher.init_pub_sub()
            #philosopher.arm()
            philosopher.takeoff(10)
            philosopher.change2Guided()
            while True:
                if philosopher.check_waypoint_reached():
                    if i < len(wplist):
                        philosopher.set_destination(wplist[i].x,wplist[i].y,wplist[i].z,wplist[i].psi)
                        i+=1
                    else:
                        philosopher.land()
        elif x == 10:
            pass
        else:
            exit()

if __name__ == "__main__":
    try:
        main()
    except:
        rospy.logerr("Exception occured while main...")
