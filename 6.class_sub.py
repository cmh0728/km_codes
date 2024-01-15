#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from std_msgs.msg import Int32

class Class_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("wego_sub_node") #1.node의 이름 설정. 
        rospy.Subscriber("/counter",Int32,callback=self.CB)


    def CB(self,msg):
        print(msg.data*3)


def main(): # main()함수 작성
    try : 
        class_sub = Class_sub()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()