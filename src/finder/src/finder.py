#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import rospy
from std_msgs.msg import UInt64, Float32
from detective import Detective, Shape

class Finder:
    # Replace the device_id parameter with your video dev. id
    def __init__(self,device_id=2):
        # Image Capture
        self.cap = cv.VideoCapture(device_id)
        # Init Shape
        self.shape = Shape(0,70,3000,8000,np.array([173,84,91]),np.array([53,48,68]))
        # Init Finder Node
        rospy.init_node("finder", anonymous=True)
        # Init Publisher center X
        self.pub_cx = rospy.Publisher("cx",UInt64,queue_size=20)
        # Init Publisher center Y
        self.pub_cy = rospy.Publisher("cy",UInt64,queue_size=20)
        # Init rate of message cycle
        self.rate = rospy.Rate(1)

    def detect(self):
        _, fra = self.cap.read()
        self.detective = Detective(self.shape, fra, verbose=False)
        img,cx,cy = self.detective.detectBySobelAndCanny()
        if cx!=None and cy!=None:
            print("Found @ ({},{})".format(cx,cy))
        return (cx,cy)

    def publish(self,cx,cy):
        if cx!=None and cy != None:
            self.pub_cx.publish(cx)
            self.pub_cy.publish(cy)
        self.rate.sleep()

def main():
    finder = Finder(2)
    while True:
        cx,cy=finder.detect()
        finder.publish(cx,cy)

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
