#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

velocity_x = rospy.get_param('/human_velocity_publisher/human_left_velocity_x')
velocity_y = rospy.get_param('/human_velocity_publisher/human_left_velocity_y')

class human_velocity_publisher():
  def __init__(self):
    self.human_velocity_pub = rospy.Publisher('/cmd_vel_human', Twist, queue_size=10)
    self.vel_msg = Twist()
    self.ctrl_c = False
    self.rate = rospy.Rate(10)
    rospy.on_shutdown(self.shutdownhook)

  def publish_vel_msg(self):
    while not self.ctrl_c:
      self.human_velocity_pub.publish(self.vel_msg)
      self.rate.sleep()
        
  def shutdownhook(self):    
    self.human_velocity_pub.publish(Twist())
    rospy.sleep(1)
    self.ctrl_c = True

  def get_velocity(self):       
    self.vel_msg.linear.x = velocity_x
    self.vel_msg.linear.y = velocity_y
    self.publish_vel_msg()

if __name__=='__main__':
  rospy.init_node('human_velocity_publisher')
  human_velocity_publisher_object = human_velocity_publisher()
  try:
    human_velocity_publisher_object.get_velocity()
  except rospy.ROSInterruptException:
    pass

