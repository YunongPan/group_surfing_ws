#!/usr/bin/env python

import rospy
import time
from geometry_msgs.msg import Twist

def human_velocity_publisher():
  rospy.init_node('human_velocity_publisher')
  human_velocity_pub = rospy.Publisher('/cmd_vel_human', Twist, queue_size=10)
  
  vel_msg =Twist()
  vel_msg.linear.x = 0.5

  rate=rospy.Rate(1)



  while not rospy.is_shutdown():
    
    
    human_velocity_pub.publish(vel_msg)
    vel_msg.linear.x += 0.01
    rate.sleep()
  




if __name__=='__main__':
  time.sleep(10)
  try:
    human_velocity_publisher()
  except rospy.ROSInterruptException:
    pass
