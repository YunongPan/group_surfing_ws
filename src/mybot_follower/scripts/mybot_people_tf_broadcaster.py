#!/usr/bin/env python
import rospy
import roslib
roslib.load_manifest('mybot_follower')
import time
import math
import tf
import geometry_msgs.msg
import numpy
from nav_msgs.msg import Odometry
from spencer_tracking_msgs.msg import TrackedPersons

class MySubscriber(object):
  def __init__(self):
    self.goal_x = rospy.get_param('/mybot_people_tf_broadcaster/goal_x')
    self.goal_y = rospy.get_param('/mybot_people_tf_broadcaster/goal_y') # Goal position
    self.max_robot_velocity = rospy.get_param('/mybot_people_tf_broadcaster/max_robot_velocity') # The maximum speed of the robot.
    self.max_direction_difference = rospy.get_param('/mybot_people_tf_broadcaster/max_direction_difference') 
    # The angle between the moving direction of the human and the direction of the line connecting
    # the robot to the goal must not be greater than this value.

    self.odom_position_x = 0.0
    self.odom_position_y = 0.0
    self.odom_direction_x = 0.0
    self.odom_direction_y = 0.0
    self.odom_direction_abs = 0.0

    self.people_velocity_x = 0.0
    self.people_velocity_y = 0.0
    self.people_velocity_abs = 0.0   
 
    self.dot_product = 0.0
    self.angle = 0.0

    self.people_name = "people1" 
    self.br = tf.TransformBroadcaster()

    rospy.Subscriber("/odom", Odometry, self.odom_callback, queue_size=1)
    rospy.Subscriber("/tracked_persons_filtered", TrackedPersons, self.people_callback, queue_size=1)   

  def odom_callback(self,msg):
    self.odom_position_x = msg.pose.pose.position.x
    self.odom_position_y = msg.pose.pose.position.y
    self.odom_direction_x = self.goal_x - self.odom_position_x
    self.odom_direction_y = self.goal_y - self.odom_position_y
    self.odom_direction_abs = math.sqrt(self.odom_direction_x ** 2 + self.odom_direction_y ** 2)   

  def people_callback(self,msg):
    people_number = len(msg.tracks)
    if people_number > 0:
      angle_all = numpy.zeros(people_number)
      velocity_all = numpy.zeros(people_number)
      velocity_all_same_direction = numpy.zeros(people_number)
      for i in range(people_number):
        self.robot_to_people_x = msg.tracks[i].pose.pose.position.x - self.odom_position_x 
        self.robot_to_people_y = msg.tracks[i].pose.pose.position.y - self.odom_position_y
        self.people_position_dot_product = self.robot_to_people_x * self.odom_direction_x + self.robot_to_people_y * self.odom_direction_y

        self.people_velocity_x = msg.tracks[i].twist.twist.linear.x
        self.people_velocity_y = msg.tracks[i].twist.twist.linear.y
        self.people_velocity_abs = math.sqrt(self.people_velocity_x ** 2 + self.people_velocity_y ** 2)
        velocity_all[i] = self.people_velocity_abs
        
        if self.people_velocity_abs > 0.05 and self.people_velocity_abs < self.max_robot_velocity and self.people_position_dot_product > 0: 
        # Exclude people who do not move, move too fast or move behind the robot.
          self.people_velocity_dot_product = self.people_velocity_x * self.odom_direction_x + self.people_velocity_y * self.odom_direction_y
          self.angle = math.acos(self.people_velocity_dot_product / (self.odom_direction_abs * self.people_velocity_abs))
          angle_all[i] = self.angle
        else: 
          angle_all[i] = 4 # The directions of people who do not move, move too fast or move behind the robot are set to 4 rad to exclude them.

      # The angle between the moving direction of the human and the direction of the line connecting
      # the robot to the goal must not be greater than 30 Grad. (It depends on self.max_direction_difference.)
      # Set the directions of people, who do not move towards the goal, to 4 rad to exclude them. Then choose the fastest people.
      same_direction_index = numpy.where(angle_all < self.max_direction_difference)
      same_direction_index_list = same_direction_index[0].tolist()
      if same_direction_index_list:
        velocity_all_same_direction[same_direction_index_list] = velocity_all[same_direction_index_list]
        velocity_all_same_direction_list = velocity_all_same_direction.tolist()
        people_index = velocity_all_same_direction_list.index(max(velocity_all_same_direction_list))

        self.br.sendTransform((msg.tracks[people_index].pose.pose.position.x, msg.tracks[people_index].pose.pose.position.y, 0), 
	  	         tf.transformations.quaternion_from_euler(0, 0, 0),
		         rospy.Time.now(),
		         self.people_name,
		         "odom")
        
      else:        
        self.br.sendTransform((self.odom_position_x, self.odom_position_y, 0), 
	  	         tf.transformations.quaternion_from_euler(0, 0, 0),
		         rospy.Time.now(),
		         self.people_name,
		         "odom")

    else:
      pass  

  def loop(self):
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('mybot_people_tf_broadcaster')    
    my_subs = MySubscriber()
    my_subs.loop()

