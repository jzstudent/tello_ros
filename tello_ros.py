#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import cv2
import tello_new as tello
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import threading
def callback(data,drone):
	command=data.data
	drone.send_command(command)

def sub_ros():
	rospy.Subscriber("command",String,callback,drone)
	#rospy.spin()

drone = tello.Tello('', 8888)
rospy.init_node('tello_state')
state_pub = rospy.Publisher('tello_state',String, queue_size=3)
img_pub = rospy.Publisher('tello_img',Image, queue_size=5)
sub_thread = threading.Thread(target=sub_ros)
sub_thread.start()

try:
	while not rospy.is_shutdown():
		tello_state=drone.read_state()
		tello_state="".join(tello_state)
		#print(tello_state)

		state_pub.publish(tello_state)
		frame=drone.read_frame()
		if frame is None or frame.size == 0:
			continue
		img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
		#img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		#cv2.imshow("img", img)
		#cv2.waitKey(1)

		try:
			img_msg = CvBridge().cv2_to_imgmsg(img, 'bgr8')
			img_msg.header.frame_id = rospy.get_namespace()
		except CvBridgeError as err:
			rospy.logerr('fgrab: cv bridge failed - %s' % str(err))
			continue
		img_pub.publish(img_msg)
		
		
		#data=rospy.wait_for_message("command",String, timeout=None)
		#callback(data,drone)
except rospy.ROSInterruptException:
	pass

