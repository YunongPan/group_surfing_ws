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
        
        if distance > 1.5:
            angular = 2 * math.atan2(trans[1], trans[0])
            linear = 0.3 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            
            cmd.linear.x = linear
            cmd.angular.z = angular
        else:
            cmd.linear.x = 0
            cmd.angular.z = 0
        mybot_vel.publish(cmd)

        rate.sleep()
