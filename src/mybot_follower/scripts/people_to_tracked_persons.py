#!/usr/bin/env python
import rospy
import roslib
roslib.load_manifest('mybot_follower')
import time
import math
import tf
import geometry_msgs.msg
from spencer_tracking_msgs.msg import TrackedPersons, TrackedPerson
from people_msgs.msg import People

tracked_persons_pub = rospy.Publisher('/tracked_persons', TrackedPersons, queue_size=50)
vx = 0.000001
vy = 0.0
theta = 0.0



def peopleCallback(msg):
  trackedpersons = TrackedPersons()
  trackedpersons.header = msg.header
  tracks_dict = dict()
  for i in range(len(msg.people)):
    tracks_dict[i] = TrackedPerson()

  tracks = list(tracks_dict.values())
  trackedpersons.tracks = tracks 



  for i in range(len(msg.people)):    
    trackedpersons.tracks[i].track_id = i
    trackedpersons.tracks[i].is_matched = True
    trackedpersons.tracks[i].pose.pose.position = msg.people[i].position
    trackedpersons.tracks[i].pose.pose.position.z = 0.0
    trackedpersons.tracks[i].twist.twist.linear = msg.people[i].velocity
    trackedpersons.tracks[i].twist.twist.linear.z = 0.0
    vx = msg.people[i].velocity.x
    vy = msg.people[i].velocity.y
    if vx < 0.05 and vx > -0.05:
      vx = 0.000001
    if vy < 0.05 and vy > -0.05:
      vy = 0.0001
    theta = math.atan(vy/vx)
    orientation_quat = tf.transformations.quaternion_from_euler(0, 0, theta)
#    test = tf.transformations.quaternion_from_euler(0, 0, 0.785398)
    trackedpersons.tracks[i].pose.pose.orientation.x = 0
    trackedpersons.tracks[i].pose.pose.orientation.y = 0
    trackedpersons.tracks[i].pose.pose.orientation.z = orientation_quat[2]
    trackedpersons.tracks[i].pose.pose.orientation.w = orientation_quat[3]
    




  tracked_persons_pub.publish(trackedpersons)



def people_subscriber():
  rospy.init_node('people_2_tracked_person')
  rospy.Subscriber("/people", People, peopleCallback)
  rospy.spin()


if __name__ == '__main__':
    people_subscriber()
