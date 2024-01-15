#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from math import *

class lidar_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("wego_sub_node") #1.node의 이름 설정. 
        rospy.Subscriber("/lidar2D",LaserScan,callback=self.lidar_CB)
        self.lazerscan_msg = LaserScan()
        

    def lidar_CB(self,msg):
        self.lazerscan_msg = msg
        min_degree = self.lazerscan_msg.angle_min *180/pi
        max_degree = self.lazerscan_msg.angle_min *180/pi
        print(min_degree,max_degree)
        
def main(): # main()함수 작성
    try : 
        class_sub = lidar_sub()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()


##라이다 값은 라디안 단위로 나옴 >>pi를 이용해서 degree로 변환