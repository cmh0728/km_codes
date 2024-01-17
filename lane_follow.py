#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Float64 #velocitiy and steer
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
        rospy.init_node("lane_follow_node") #1.node의 이름 설정. 

        #publisher(vel)
        self.pub = rospy.Publisher("/commands/motor/speed",Float64,queue_size=1) #topic명 제대로 입력해야 함.
        self.pub = rospy.Publisher("/commands/servo/position",Float64,queue_size=1) #topic명 제대로 입력해야 함.

        self.cmd_msg = Float64()
        self.rate = rospy.Rate(10)
        self.speed = 0
        self.steer = 0 #value : 0~1 --> degree : -19.5~19.5

        rospy.Subscriber("/image_jpeg/compressed",CompressedImage,callback=self.Camera_CB)
        self.image_msg = CompressedImage()
        self.bridge = CvBridge()


        # houghLine_pub = rospy.Publisher('HoughLine', Int32MultiArray, queue_size=5)
        # self.pts = []
        # self.cte_pub = rospy.Publisher('/LaneFollow', Float64, queue_size=1)
        # self.rate = rospy.Rate(50)
        # self.bridge = CvBridge()
        # self.offset = 0.41259
        # self.middle = 0.546
        # self.gain = 0
        # self.semaphore = True
        # self.count = 0
        # self.pixelRate_sd = (250-50)/(360-260) # 원근법을 고려한 중앙까지 간격 보상(가까울수록 많이)
        # self.pixelRate_km = (138-38)/(400-313)
        # self.xThresh_sd = 50 # 가장 멀리 HL 잡혔을 때 중앙까지 간격
        # self.yThresh_sd = 260
        # self.xThresh_km = 33
        # self.yThresh_km = 313
        # self.distance_sd = 160 # 송도트랙 차선과 중심간의 거리
        # self.lanewidth_sd = 0.275
        # self.distance_km = 115 # 국민대 차선과 중심간의 거리
        # self.lanewidth_km = 0.175
        # self.error = 0

    def Camera_CB(self,msg):
        # np.array([])
        self.image_msg = msg
        cv_img = self.bridge.compressed_imgmsg_to_cv2(self.image_msg) #cv형태로 이미지 형식 변환
        hsv_img = cv2.cvtColor(cv_img,cv2.COLOR_BGR2HSV) #hsv이미지로 채널 변경
        # cv2.imshow("cv_img",cv_img) #원본 이미지 확인
        # cv2.imshow("hsv_img",hsv_img) #hsv이미지 확인

        kernel_size = 5

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
        # cv2.imshow('yello&white',combined_img)
        # cv2.imshow("filtered_img",filtered_img)


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
        img_params = np.float32([[width/2-150,0],[width/2-150,height],[width/2+150,height],[width/2+150,0]])
        mat = cv2.getPerspectiveTransform(corner_points_array,img_params)
        minverse = cv2.getPerspectiveTransform(img_params,corner_points_array) #원상복구 시키기 위한 변수
        image_transformed = cv2.warpPerspective(filtered_img,mat,(width,height))
        cv2.imshow("Bird_eye_view",image_transformed)
        

        #Rejon of interest >>정지선 인식에 방해되서 폐기
        # x = int(cv_img.shape[1])
        # y = int(cv_img.shape[0])
        # # 한 붓 그리기
        # _shape = np.array(
        #     [[int(0.1*x), int(y)], [int(0.1*x), int(0.1*y)], [int(0.4*x), int(0.1*y)], [int(0.4*x), int(y)], [int(0.7*x), int(y)], [int(0.7*x), int(0.1*y)],[int(0.9*x), int(0.1*y)], [int(0.9*x), int(y)], [int(0.2*x), int(y)]])

        # mask = np.zeros_like(image_transformed)

        # if len(image_transformed.shape) > 2:
        #     channel_count = image_transformed.shape[2]
        #     ignore_mask_color = (255,) * channel_count
        # else:
        #     ignore_mask_color = 255

        # cv2.fillPoly(mask, np.int32([_shape]), ignore_mask_color)
        # masked_image = cv2.bitwise_and(image_transformed, mask)
        # cv2.imshow("masked",masked_image)


        #gray_scale_transform
        gray_img = cv2.cvtColor(image_transformed,cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray",gray_img)

        #이진화,threshold
        ret, thresh = cv2.threshold(gray_img, 160, 255, cv2.THRESH_BINARY)
        cv2.imshow("thresh",thresh)

       
        histogram = np.sum(thresh[thresh.shape[0]//2:, :], axis=0)
        midpoint = np.int32(histogram.shape[0]/2)
        leftbase = np.argmax(histogram[:midpoint])
        rightbase = np.argmax(histogram[midpoint:]) + midpoint

        # 왼쪽 차선, 오른쪽 차선 base확인
        # print(leftbase,rightbase)

        #window roi, sliding window search
        out_img = np.dstack((thresh, thresh, thresh))

        nwindows = 6
        window_height = np.int32(thresh.shape[0] / nwindows)
        nonzero = thresh.nonzero()  # 선이 있는 부분의 인덱스만 저장 
        nonzero_y = np.array(nonzero[0])  # 선이 있는 부분 y의 인덱스 값
        nonzero_x = np.array(nonzero[1])  # 선이 있는 부분 x의 인덱스 값 
        margin = 100
        minpix = 50
        left_lane = []
        right_lane = []
        color = [0, 255, 0]
        thickness = 2

        for w in range(nwindows):
            win_y_low = thresh.shape[0] - (w + 1) * window_height  # window 윗부분
            win_y_high = thresh.shape[0] - w * window_height  # window 아랫 부분
            win_xleft_low = leftbase - margin  # 왼쪽 window 왼쪽 위
            win_xleft_high = leftbase + margin  # 왼쪽 window 오른쪽 아래
            win_xright_low = rightbase - margin  # 오른쪽 window 왼쪽 위 
            win_xright_high = rightbase + margin  # 오른쪽 window 오른쪽 아래

            cv2.rectangle(out_img, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), color, thickness)
            cv2.rectangle(out_img, (win_xright_low, win_y_low), (win_xright_high, win_y_high), color, thickness)
            good_left = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_xleft_low) & (nonzero_x < win_xleft_high)).nonzero()[0]
            good_right = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_xright_low) & (nonzero_x < win_xright_high)).nonzero()[0]
            left_lane.append(good_left)
            right_lane.append(good_right)
            # cv2.imshow("oo", out_img)

            if len(good_left) > minpix:
                leftbase = np.int32(np.mean(nonzero_x[good_left]))
            if len(good_right) > minpix:
                rightbase = np.int32(np.mean(nonzero_x[good_right]))

        left_lane = np.concatenate(left_lane)  # np.concatenate() -> array를 1차원으로 합침
        right_lane = np.concatenate(right_lane)

        leftx = nonzero_x[left_lane]
        lefty = nonzero_y[left_lane]
        rightx = nonzero_x[right_lane]
        righty = nonzero_y[right_lane]

        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

        ploty = np.linspace(0, thresh.shape[0] - 1, thresh.shape[0])
        left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
        right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

        ltx = np.trunc(left_fitx)  # np.trunc() -> 소수점 부분을 버림
        rtx = np.trunc(right_fitx)

        out_img[nonzero_y[left_lane], nonzero_x[left_lane]] = [255, 0, 0]
        out_img[nonzero_y[right_lane], nonzero_x[right_lane]] = [0, 0, 255]

        # plt.imshow(out_img)
        # plt.plot(left_fitx, ploty, color = 'yellow')
        # plt.plot(right_fitx, ploty, color = 'yellow')
        # plt.xlim(0, 1280)
        # plt.ylim(720, 0)
        # plt.show()

        ret = {'left_fitx' : ltx, 'right_fitx': rtx, 'ploty': ploty} #>>draw info

        #dray lane line
        #original_image, warped_image, Minv, ret
        left_fitx = ret['left_fitx']
        right_fitx = ret['right_fitx']
        ploty = ret['ploty']

        warp_zero = np.zeros_like(thresh).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        pts = np.hstack((pts_left, pts_right))

        mean_x = np.mean((left_fitx, right_fitx), axis=0)
        pts_mean = np.array([np.flipud(np.transpose(np.vstack([mean_x, ploty])))])

        cv2.fillPoly(color_warp, np.int_([pts]), (255,0,255))
        cv2.fillPoly(color_warp, np.int_([pts_mean]), (255,0,255))

        newwarp = cv2.warpPerspective(color_warp, minverse, (cv_img.shape[1], cv_img.shape[0]))
        result = cv2.addWeighted(cv_img, 1, newwarp, 0.4, 0)

        cv2.imshow("result",result)
        
        
        cv2.waitKey(1)
    
    def motor_speed(self):
        speed = 1
        if speed > 8:
            speed = 8 # 제한 범위 설정
        self.cmd_msg.data = speed * 300 #max == 2400
        self.pub.publish(self.cmd_msg)
        print(f"speed : {self.cmd_msg.data}")
        self.rate.sleep()
    
    def motor_steer(self):
        pass



def main(): # main()함수 작성
    try : 
        class_pub_sub= cam_sub()
        while not rospy.is_shutdown():
            class_pub_sub.motor_speed()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()
    
#next step : steer + vel + cb
#next step 2: pid
    
#1. left인지, right인지 판별, 차선이 하나만 뜨는 과정에서 추종, 
#2. 정지선 hough line
#3. 신호등 topic 받기