#!/usr/bin/env python
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("rgb/image_raw_color",Image,self.callback)

  def callback(self,data):
    cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    #(rows,cols,channels) = cv_image.shape
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(1)

if __name__ == '__main__':
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  rospy.spin()
  cv2.destroyAllWindows()
