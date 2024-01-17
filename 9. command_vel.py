#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from std_msgs.msg import Float64 #rostopic info를 이용해서 메세지 타입 설정

class sim_pub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("sim_cmd_node") #1.node의 이름 설정.
        self.pub = rospy.Publisher("/commands/motor/speed",Float64,queue_size=1) #topic명 제대로 입력해야 함.
        self.cmd_msg = Float64()
        self.rate = rospy.Rate(10)

    def motor(self):
        speed = 6
        if speed > 8:
            speed = 8 # 제한 범위 설정
        self.cmd_msg.data = speed * 300 #max == 2400
        self.pub.publish(self.cmd_msg)
        print(f"speed : {self.cmd_msg.data}")
        self.rate.sleep()


def main(): # main()함수 작성
    try : 
        class_pub = sim_pub()
        while not rospy.is_shutdown():
            class_pub.motor()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()