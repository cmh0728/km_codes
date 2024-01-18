#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import rospy
from morai_msgs.msg import GetTrafficLightStatus
from std_msgs.msg import Float64 

class Traffic_light_sub: 
    def __init__(self) :
        rospy.Subscriber("/GetTrafficLightStatus",GetTrafficLightStatus,callback=self.Traffic_light_CB)
        self.prev_light_status = None 
        self.steer_pub = steer_pub()
        self.speed_pub = speed_pub()

    def Traffic_light_CB(self,msg):
        current_light_status = msg.trafficLightStatus
        if self.prev_light_status is not None and self.prev_light_status != current_light_status:  
            if current_light_status == 1:
                print("빨간불입니다.정지")
                self.steer_pub.steer = 0.5
                self.speed_pub.speed = 0
            elif current_light_status == 16:
                print("파란불입니다.")
                self.steer_pub.steer = 0.5 
                self.speed_pub.speed = 0  
            elif current_light_status == 4:
                print("노란불입니다.")
                self.steer_pub.steer = 0.5  
                self.speed_pub.speed = 0  
            elif current_light_status == 33:
                print("좌회전신호입니다.")
                self.steer_pub.steer = 0.345
                self.speed_pub.speed = 4
        self.prev_light_status = current_light_status 

class steer_pub: 
    def __init__(self) :
        self.pub = rospy.Publisher("/commands/servo/position",Float64,queue_size=1) 
        self.cmd_msg = Float64()
        self.rate = rospy.Rate(1)
        self.steer = 0

    def steering(self):
        self.cmd_msg.data = self.steer
        self.pub.publish(self.cmd_msg)
        print(f"steer:{self.cmd_msg.data}")
        self.rate.sleep()

class speed_pub: 
    def __init__(self) :
        self.pub = rospy.Publisher("/commands/motor/speed",Float64,queue_size=1) 
        self.cmd_msg = Float64()
        self.rate = rospy.Rate(1)
        self.speed = 0

    def motor_speed(self):
        self.cmd_msg.data = self.speed * 300
        self.pub.publish(self.cmd_msg)
        print(f"speed : {self.cmd_msg.data}")
        self.rate.sleep()

def main(): 
    rospy.init_node("TrafficLight_node")
    try : 
        class_TrafficLight = Traffic_light_sub()
        while not rospy.is_shutdown():
            class_TrafficLight.steer_pub.steering()
            class_TrafficLight.speed_pub.motor_speed()  
        rospy.spin()

    except rospy.ROSInterruptException:
        pass

if __name__== "__main__":
    main()
