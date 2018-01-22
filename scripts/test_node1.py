#!/usr/bin/env python

import rospy
from std_msgs.msg import String

if __name__== "__main__":
    rospy.init_node('datacol_node1') # Resgistering node in ros master
    rospy.loginfo('Welcome to ROS')
    
