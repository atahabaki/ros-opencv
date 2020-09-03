#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import math
import rospy
from std_msgs.msg import UInt64, Float32
from detective import Detective, Shape

class Finder:
    _NODE_NAME="finder"
    _NODE_CX="finder/cx"
    _NODE_CY="finder/cy"
    _NODE_DIST="finder/distance"
    _NODE_DIST_PERC="finder/distance_perc"
    _NODE_ANGLE="finder/angle"
    _WIDTH=400
    _HEIGHT=300
    # Replace the device_id parameter with your video dev. id
    def __init__(self,device_id=2):
        # Image Capture
        self.cap = cv.VideoCapture(device_id)
        # Init Shape
        self.shape = Shape(0,70,3000,8000,np.array([173,84,91]),np.array([53,48,68]))
        # Init Finder Node
        rospy.init_node(self._NODE_NAME, anonymous=True)
        # Init Publisher center X
        self.pub_cx = rospy.Publisher(self._NODE_CX,UInt64,queue_size=10)
        # Init Publisher center Y
        self.pub_cy = rospy.Publisher(self._NODE_CY,UInt64,queue_size=10)
        # Distance Publisher
        self.pub_dist = rospy.Publisher(self._NODE_DIST,Float32,queue_size=10)
        # Distance Percentage Publisher
        self.pub_dist_perc = rospy.Publisher(self._NODE_DIST_PERC,Float32,queue_size=10)
        # Angle Publisher
        self.pub_angle = rospy.Publisher(self._NODE_ANGLE,Float32,queue_size=10)
        # Init rate of message cycle
        self.rate = rospy.Rate(1)

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
        return dist/distance*100

    def calcAngle(self,dx,dy):
        return math.atan(dx/dy)

    def calculate(self,cx,cy):
        dx=self.calcDistanceX(cx)
        dy=self.calcDistanceX(cy)
        distance=self.calcDistance(dx,dy)
        distperc=self.calcDistancePercentage(distance)
        angle=self.calcAngle(dx,dy)
        return (distance,distperc,angle)

    def detect(self):
        _, fra = self.cap.read()
        #self.detective = Detective(self.shape, fra, verbose=False)
        #img,cx,cy = self.detective.detectBySobelAndCanny(dimens=(self._WIDTH,self._HEIGHT))
        img,cx,cy=0,0,0
        dist,dist_perc,ang=self.calculate(cx,cy)
        if cx!=None and cy!=None:
            print("Found @ ({},{})".format(cx,cy))
        return (cx,cy,dist,dist_perc,ang)

    def publish(self,cx,cy,dist,dist_perc,ang):
        if cx!=None and cy != None:
            self.pub_cx.publish(cx)
            self.pub_cy.publish(cy)
            self.pub_dist.publish(dist)
            self.pub_dist_perc.publish(dist_perc)
            self.pub_angle.publish(ang)
        self.rate.sleep()

def main():
    finder = Finder(2)
    while True:
        cx,cy,dist,dist_perc,ang=finder.detect()
        finder.publish(cx,cy,dist,dist_perc,ang)

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
