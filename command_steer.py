#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from std_msgs.msg import Float64 #rostopic info를 이용해서 메세지 타입 설정

class steer_pub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("sim_cmd_node") #1.node의 이름 설정.
        self.pub = rospy.Publisher("/commands/servo/position",Float64,queue_size=1) #topic명 제대로 입력해야 함.
        self.cmd_msg = Float64()
        self.rate = rospy.Rate(10)
        self.steer = 0 # value : 0~1 --> degree : -19.5~19.5 
        #0.5가 중앙 셋팅

    def steering(self):
        # self.steer += 0.01
        # if self.steer>=1.0:
        #     self.steer =1.0 
        # self.cmd_msg.data = self.steer
        self.cmd_msg.data = 0.5
        self.pub.publish(self.cmd_msg)
        print(f"steer:{self.cmd_msg.data}")
        self.rate.sleep()

def main(): # main()함수 작성
    try : 
        class_pub = steer_pub()
        while not rospy.is_shutdown():
            class_pub.steering()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()