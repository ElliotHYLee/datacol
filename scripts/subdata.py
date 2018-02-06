#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu, Image, NavSatFix
from cv_bridge import CvBridge, CvBridgeError
import cv2


class SubData:
    def __init__(self):
        self.file = open("Data/data.txt", "w")
        self.bridge = CvBridge()
        self.fileLock = 1
        self.dummyCounter = 0
        self.counter = 0
        self.gps = None
        self.listener()

  
    def cbImu(self, data):
        q = data.orientation

        if self.fileLock == 0:
            if self.dummyCounter<10:
                self.dummyCounter+=1
            else:
                self.file.write("%.4f %d %.6f %.6f %.6f %.6f\n" % (rospy.get_time(), self.counter, q.x, q.y, q.z, q.w))
                self.counter +=1
                self.fileLock = 1

    def cbImg(self,data):
        if self.fileLock == 1:
            if self.dummyCounter <10:
               self.dummyCounter+=1
            else:
                now = rospy.get_rostime()
                rospy.loginfo("Current time %i %i", now.secs, now.nsecs)
                cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
                #(rows,cols,channels) = cv_image.shape
                #cv2.imshow("Image window", cv_image)
                #cv2.waitKey(1)
                cv2.imwrite("Data/Image/"+str(self.counter) + ".jpg", cv_image)
                self.fileLock = 0

    def callBack(self,Nav):
        if self.fileLock ==0:
            self.fileLock = 1
            self.file.write("%.4f %d %.6f %.6f\n" % (rospy.get_time(), self.counter, Nav.latitude, Nav.longitude))
            #rospy.loginfo('I heard %s', Nav.latitude)
            #rospy.loginfo('I heard %s', Nav.longitude)
            self.fileLock = 0
        else:
            while self.fileLock==1:
                aaaa = 1
            self.fileLock = 1
            self.file.write("%.4f %d %f %f\n" % (rospy.get_time(), self.counter, Nav.latitude, Nav.longitude))
            #rospy.loginfo('I heard %s', Nav.latitude)
            #rospy.loginfo('I heard %s', Nav.longitude)
            self.fileLock = 0
        

    def listener(self):
        rospy.init_node('mavlisten', anonymous=True)
        
        rospy.Subscriber("rgb/image_raw_color",Image,self.cbImg)
        rospy.Subscriber('mavros/imu/data', Imu, self.cbImu)
        rospy.Subscriber('/mavros/global_position/raw/fix', NavSatFix, self.callBack)
        rospy.spin()


if __name__ == '__main__':
    mav = SubData()    

    
