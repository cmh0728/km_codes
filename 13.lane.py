#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import cv2

class cam_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("lane_detecton_node") #1.node의 이름 설정. 
        rospy.Subscriber("/image_jpeg/compressed",CompressedImage,callback=self.Camera_CB)
        self.image_msg = CompressedImage()
        self.bridge = CvBridge()

    def Camera_CB(self,msg):
        self.image_msg = msg
        cv_img = self.bridge.compressed_imgmsg_to_cv2(self.image_msg) #cv형태로 이미지 형식 변환
        cv2.imshow("cv_img",cv_img)
        cv2.waitKey(1)

def main(): # main()함수 작성
    try : 
        class_sub = cam_sub()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()