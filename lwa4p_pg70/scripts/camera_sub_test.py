#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image as ImageMsg
from cv_bridge import CvBridge
from PIL import Image, ImageOps

remastered_frame = None

def show_image(img):
    cv2.imshow("Frame",img)
    cv2.waitKey(1)

def image_callback(data):
    br = CvBridge()
    # rospy.loginfo('Subscribing Video Frame')
    rec_frame = br.imgmsg_to_cv2(data)
    remastered_frame = cv2.cvtColor(rec_frame,cv2.COLOR_BGR2RGB)
    show_image(remastered_frame)
    
    
def recieve_message():
    topic_name = "image_feed"
    # topic_name = input("Name of the topic : ")
    rospy.init_node('video_subscriber',anonymous=True)
    rospy.Subscriber(topic_name,ImageMsg,image_callback)
    rospy.spin()
    cv2.destroyAllWindows()
    
    
    
if __name__ == '__main__':
    recieve_message()
