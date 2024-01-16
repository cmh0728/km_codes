#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import numpy as np  
import cv2 
import matplotlib.pyplot as plt


# numpy : 행렬을 다룰 때 주로 사용하는 모듈
# open cv에서는 BGR형태, np행렬의 shape은 행, 렬 
# 이미지 기본 크기 : 480,640 ( y , x )
#cv2.split으로 구성성분(bgr, hsv)로 구분해서 볼 수 있음
#cv2.cvtColor(img,cv2.COLOR_BGR2HSV)를 이용해서 bgr이미지를 hsv로 변경 할 수 있음

class cam_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("lane_detecton_node") #1.node의 이름 설정. 
        rospy.Subscriber("/image_jpeg/compressed",CompressedImage,callback=self.Camera_CB)
        self.image_msg = CompressedImage()
        self.bridge = CvBridge()

    def Camera_CB(self,msg):
        # np.array([])
        self.image_msg = msg
        cv_img = self.bridge.compressed_imgmsg_to_cv2(self.image_msg) #cv형태로 이미지 형식 변환
        hsv_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2HSV) #hsv이미지로 채널 변경
        # cv2.imshow("cv_img",cv_img) #원본 이미지 확인
        # cv2.imshow("hsv_img",hsv_img) #hsv이미지 확인

        kernel_size = 5
        #gray_scale_transform
        # gray_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray",gray_img)

        #gaussian_blur
        # blur_gray = cv2.GaussianBlur(gray_img,(kernel_size,kernel_size),0)
        # cv2.imshow("blur_gray",blur_gray)

        yellow_lower = np.array([15,128,0])
        yellow_upper = np.array([40,255,255])
        yellow_range = cv2.inRange(hsv_img,yellow_lower,yellow_upper)
        white_lower = np.array([0,0,192])
        white_upper = np.array([179,64,255])
        white_range = cv2.inRange(hsv_img,white_lower,white_upper)
        combined_img = cv2.bitwise_or(yellow_range,white_range)
        filtered_img = cv2.bitwise_and(cv_img,cv_img,mask=combined_img)
        # cv2.imshow("yellow",yellow_range)
        # cv2.imshow("white",white_range)
        cv2.imshow('yello&white',combined_img)
        cv2.imshow("filtered_img",filtered_img)


        # blur_img = cv2.GaussianBlur(combined_img,(kernel_size,kernel_size),0)
        # cv2.imshow("blur_gray",blur_img)

        #bird_eye_view >>>되도록 수정 xxxx
        # 좌하 46,426
        # 좌상 267,274
        # 우상 370,274
        # 우하 560,423

        corner_points_array = np.float32([[267,274],[46,426]
                                          ,[560,423],[370,274]]) #좌상, 좌하, 우하, 우상
        height, width = cv_img.shape[:2]
        gray_img_params = np.float32([[width/2-150,0],[width/2-150,height],[width/2+150,height],[width/2+150,0]])
        mat = cv2.getPerspectiveTransform(corner_points_array,gray_img_params)
        image_transformed = cv2.warpPerspective(filtered_img,mat,(width,height))
        cv2.imshow("Bird_eye_view",image_transformed)

        
        
        
        
        
        
        cv2.waitKey(1)

def main(): # main()함수 작성
    try : 
        class_sub = cam_sub()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()
    