#!/usr/bin/env python
import cv2 as cv
import numpy as np
import math
import rospy
from finder.msg import Where
from detective import Detective, Shape

# TODO (1) Change print statements to rospy logs...
# TODO (2) Rewrite for Where message type instead of std_msgs

class Finder:
    _NODE_NAME="finder"
    _NODE_WHERE="finder/where"
    _WIDTH=400
    _HEIGHT=300
    """
    ?>5000 is non-sense for this algorithm (meaning do not care if you face with them)
    """
    _OUT_LIMIT_INT=5000
    _OUT_LIMIT_FLOAT=5000.0
    # Replace the device_id parameter with your video dev. id
    def __init__(self,device_id=2):
        # Image Capture
        self.cap = cv.VideoCapture(device_id)
        # Init Shape
        self.shape = Shape(0,70,3000,8000,np.array([173,84,91]),np.array([53,48,68]),20,100000)
        # Init Finder Node
        #rospy.init_node(self._NODE_NAME, anonymous=True)
        rospy.init_node(self._NODE_NAME)
        # Init Publisher center X
        self.pub_where = rospy.Publisher(self._NODE_WHERE,Where,queue_size=10)
        # Init rate of message cycle
        self.rate = rospy.Rate(10)

    def calcDistanceX(self,cx):
        return self._WIDTH/2-cx

    def calcDistanceY(self,cy):
        return self._HEIGHT/2-cy

    def calcDistance(self,dx,dy):
        distance=math.sqrt(dx**2+dy**2)
        return distance

    def calcDistancePercentage(self,distance):
        hx=self._WIDTH/2
        hy=self._HEIGHT/2
        dist=math.sqrt(hx**2+hy**2)
        if dist != 0:
            return distance/dist*100
        else:
            return self._OUT_LIMIT_FLOAT

    def calcAngle(self,dx,dy):
        if dy != 0:
            return math.atan(dx/dy)
        else:
            return self._OUT_LIMIT_FLOAT

    def calculate(self,cx,cy):
        if cx==None and cy==None:
            cx,cy=self._OUT_LIMIT_INT,self._OUT_LIMIT_INT
        dx=self.calcDistanceX(cx)
        dy=self.calcDistanceX(cy)
        distance=self.calcDistance(dx,dy)
        distperc=self.calcDistancePercentage(distance)
        angle=self.calcAngle(dx,dy)
        return (distance,distperc,angle)

    def detect(self,open_window=False):
        _, fra = self.cap.read()
        self.detective = Detective(self.shape, fra, verbose=False)
        img,cx,cy = self.detective.detectReds(dimens=(self._WIDTH,self._HEIGHT))
        if open_window:
            cv.imshow("img",img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                exit(0)
        return (cx,cy)

    def publish(self,cx,cy,dist,dist_perc,ang):
        where = Where()
        if cx==None and cy==None:
            cx,cy=self._OUT_LIMIT_INT,self._OUT_LIMIT_INT
            dist,dist_perc,ang=self._OUT_LIMIT_FLOAT,self._OUT_LIMIT_FLOAT,self._OUT_LIMIT_FLOAT
        where.cx = cx
        where.cy = cy
        where.distance = dist
        where.distance_perc = dist_perc
        where.angle = ang
        self.pub_where.publish(where)

    def sleep(self):
        self.rate.sleep()

    def log_info(self,cx,cy,dist,dist_perc,ang):
        rospy.loginfo("Found @ ({},{}), distance: {}, distance (%): {}%, angle: {}".format(cx,cy,dist,dist_perc,ang))

def main():
    finder = Finder(0)
    while True:
        cx,cy=finder.detect(open_window=True)
        dist,dist_perc,ang=finder.calculate(cx,cy)
        finder.log_info(cx,cy,dist,dist_perc,ang)
        finder.publish(cx,cy,dist,dist_perc,ang)
        finder.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
