#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image as ImageMsgs
from cv_bridge import CvBridge
import cv2

def publish_message():
    my_publisher = rospy.Publisher('image_feed',ImageMsgs,queue_size=10)
    rospy.init_node('video_publisher',anonymous=True)
    rate = rospy.Rate(30)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    br = CvBridge()
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        if ret == True:
            rospy.loginfo('publishing video frame')
            my_publisher.publish(br.cv2_to_imgmsg(frame))
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_message()
    except rospy.ROSInterruptException:
        pass