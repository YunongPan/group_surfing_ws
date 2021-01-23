#!/usr/bin/env python
import rospy
import roslib
roslib.load_manifest('mybot_follower')
import time
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('mybot_follower')
    listener = tf.TransformListener()
    mybot_vel = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        cmd = geometry_msgs.msg.Twist()
        try:
            (trans,rot) = listener.lookupTransform('/chassis', '/people1', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            cmd.linear.x = 0
            cmd.angular.z = 0
            mybot_vel.publish(cmd)
            continue
        distance = math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        
        if distance > 1.5:  # If the robot is less than 1.5 meters away from the person being tracked, it will stop.
            angular = 2 * math.atan2(trans[1], trans[0])
            if angular > 0.7854:  # The angular velocity shall not too fast. (Here less than 45 grads per second.)
              angular = 0.7854
            linear = 0.3 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)            
            cmd.linear.x = linear
            cmd.angular.z = angular
        else: 
            cmd.linear.x = 0
            cmd.angular.z = 0
        mybot_vel.publish(cmd)
        rate.sleep()
