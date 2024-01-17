#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
class Traffic_light_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("TrafficLight_node") #1.node의 이름 설정.
        self.pub = rospy.Publisher("/GetTrafficLightStatus",GetTrafficLightStatus,queue_size=1) #topic명 제대로 입력해야 함.


#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from morai_msgs.msg import GetTrafficLightStatus

class Traffic_light_sub: #1. class 이름 설정
    def __init__(self) : #2. init 단 설정
        rospy.init_node("TrafficLight_node") #1.node의 이름 설정. 
        rospy.Subscriber("/GetTrafficLightStatus",GetTrafficLightStatus,callback=self.Traffic_light_CB)


    def Traffic_light_CB(self,msg):
        if "trafficLightStatus" == 1: #이거 되냐?
            
            print(msg)
        pass


def main(): # main()함수 작성
    try : 
        light_sub = Traffic_light_sub()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__== "__main__": # main함수의 선언, 시작을 의미
    main()


#echo /Gettrafficlight
# header: 
#   seq: 456
#   stamp: 
#     secs: 1705484987
#     nsecs: 619000000
#   frame_id: "TrafficLightStatus"
# trafficLightIndex: "SN000005"
# trafficLightType: 2
# trafficLightStatus: 33
    

#빨간색 : 1, 파란불 : 16 노란불 4 , 직진x 좌회전신호 : 33
