#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
from math import *
import os

class lidar_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("lidar_e_stop_node") #1.node의 이름 설정. 
        self.pub = rospy.Publisher("/commands/motor/speed",Float64,queue_size=1)
        rospy.Subscriber("/lidar2D",LaserScan,callback=self.lidar_CB)
        self.scan_msg = LaserScan()
        self.speed_msg = Float64()
        

    def lidar_CB(self,msg):
        os.system("clear") #값이 들어오기 전까지는 clear해줌.
        self.lazerscan_msg = msg
        min_degree = self.lazerscan_msg.angle_min *180/pi
        max_degree = self.lazerscan_msg.angle_min *180/pi
        degree_angle_increment = self.scan_msg.angle_increment *180/pi
        # print(self.scan_msg)
        # print(min_degree,max_degree)
        #self.lazerscan_msg.ranges -->> 범위값
        degrees =  [min_degree+ degree_angle_increment*index for index, value in enumerate(self.scan_msg.ranges)] # 각도값
        obstacle= 0 #다양한 방법으로 설정할 수 있음 (정지 변수)
        for index , value in enumerate(self.scan_msg.ranges):
            if -30<degrees[index]<30 and 0<value<1.5: #장애물 발견 조건 (거리단위는 m)
                print(f"find obstacle{index} : {degrees[index]}")
                obstacle = 1
                # e_stop = True
            else : pass
                # e_stop = False

            if obstacle == 1 :
                self.speed_msg.data = 0 # data를 꼭 붙여줘야 함. 
            else :
                self.speed_msg.data = 1200


            self.pub.publish()




def main(): # main()함수 작성
    try : 
        class_sub = lidar_sub()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()


##라이다 값은 라디안 단위로 나옴 >>pi를 이용해서 degree로 변환