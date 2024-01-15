#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from math import *
import os

class lidar_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("wego_sub_node") #1.node의 이름 설정. 
        rospy.Subscriber("/lidar2D",LaserScan,callback=self.lidar_CB)
        self.lazerscan_msg = LaserScan()
        

    def lidar_CB(self,msg):
        os.system("clear") #값이 들어오기 전까지는 clear해줌.
        self.lazerscan_msg = msg
        min_degree = self.lazerscan_msg.angle_min *180/pi
        max_degree = self.lazerscan_msg.angle_min *180/pi
        degree_angle_increment = self.lazerscan_msg.angle_increment *180/pi
        print(self.lazerscan_msg)
        print(min_degree,max_degree)
        #self.lazerscan_msg.ranges -->> 범위값
        degrees =  [min_degree+ degree_angle_increment*index for index, value in enumerate(self.lazerscan_msg.ranges)] # 각도값
        for index , value in enumerate(self.lazerscan_msg.ranges):
            if -30<degrees[index]<30 and 0<value<1.5: #장애물 발견 조건 (거리단위는 m) , # 각도값, 거리값 함께 고려해서 라이다로 탐지 
                print(f"find obstacle{index} : {degrees[index]}") 




def main(): # main()함수 작성
    try : 
        class_sub = lidar_sub()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()


##라이다 값은 라디안 단위로 나옴 >>pi를 이용해서 degree로 변환