#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import String

rospy.init_node('tello_control')
command_pub = rospy.Publisher('command',String,queue_size=10)

command_pub.publish('takeoff')

command_pub.publish('go 0 10 0 10')

command_pub.publish('land')


