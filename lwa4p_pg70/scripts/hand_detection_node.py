#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import Image as ImageMsg
from geometry_msgs.msg import Pose
from cv_bridge import CvBridge
import mediapipe as mp
import numpy as np
from std_msgs.msg import String , Float32MultiArray

remastered_frame = None

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils



def hand_detection(frame):
    h,w,c = frame.shape
    result = hands.process(frame)
    hand_landmarks = result.multi_hand_landmarks
    if hand_landmarks:
        landmarks = []
        for handLMs in hand_landmarks:
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            for lm in handLMs.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.circle(frame, (int((x_min+x_max)/2),int((y_min+y_max)/2)), radius=2, color=(0, 0, 0), thickness=2)
            mpDraw.draw_landmarks(frame, handLMs, mpHands.HAND_CONNECTIONS)
            message = Float32MultiArray()
            message.data = [(x_min + x_max)/2,(y_min + y_max)/2]
        # message.position.y = (y_min + y_max)/2*0.0044
        # message.position.z = 0.5165863795721032*0.0000005
        # message.data = [(x_min + x_max)/2,(y_min + y_max)/2,0.5165863795721032]
            coord_pub.publish(message)
            print("X: "+str(((x_min + x_max)/2)*1))
            print("Y: "+str(((y_min + y_max)/2)*1))
            # print("Z: "+str(0.5165863795721032))
            # prediction = model.predict([landmarks])
            # classID = np.argmax(prediction)
            # detected_gesture = classNames[classID]
            
    # cv2.putText(frame, detected_gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            
    cv2.imshow("Hand Detection", frame)


    cv2.waitKey(1)
    # cv2.imshow("Frame",img)
    # cv2.waitKey(1)

def image_callback(data):
    br = CvBridge()
    # rospy.loginfo('Subscribing Video Frame')
    rec_frame = br.imgmsg_to_cv2(data)
    remastered_frame = cv2.cvtColor(rec_frame,cv2.COLOR_BGR2RGB)
    hand_detection(remastered_frame)
    
def recieve_message():
    global coord_pub
    # global model,classNames
    # model = load_model('/home/kaito/catkin_ws/src/lwa4p_pg70/scripts/mp_hand_gesture')
    # f = open('/home/kaito/catkin_ws/src/lwa4p_pg70/scripts/gesture.names', 'r')
    # classNames = f.read().split('\n')
    # f.close()
    topic_name = "image_feed"
    # topic_name = input("Name of the topic : ")
    rospy.init_node('video_subscriber',anonymous=True)
    rospy.Subscriber(topic_name,ImageMsg,image_callback)
    coord_pub = rospy.Publisher('co_ords',Float32MultiArray,queue_size=10)
    rospy.Rate(0.5).sleep()
    rospy.spin()
    cv2.destroyAllWindows()
    
    
    
if __name__ == '__main__':
    
    recieve_message()