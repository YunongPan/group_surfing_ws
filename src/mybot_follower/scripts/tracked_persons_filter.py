#!/usr/bin/env python
import os, sys, math, time
import roslib, rospy, tf, message_filters
import geometry_msgs.msg
import numpy
from spencer_tracking_msgs.msg import TrackedPersons, TrackedGroups

def tracked_persons_filter_Callback(trackedPersons, trackedGroups):  
  tracked_persons_index = numpy.zeros(len(trackedGroups.groups))
  trackedPersonsFiltered = trackedPersons
  closed_person_id = 0
  closed_person_distance = 50000

  for i in range(len(trackedGroups.groups)):
    if len(trackedGroups.groups[i].track_ids) == 1: # No one will be filtered out from a single-person group.
      tracked_persons_index[i] = trackedGroups.groups[i].track_ids[0]
    else: # In a multi-person group, the person closest to the robot will be kept, and the others will be filtered out.
      try:
        (trans,rot) = listener.lookupTransform('/odom', '/chassis', rospy.Time(0))
      except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        continue
      for j in range(len(trackedGroups.groups[i].track_ids)):
        grouped_person_id = trackedGroups.groups[i].track_ids[j]
        try:
          grouped_person_x = trackedPersons.tracks[grouped_person_id].pose.pose.position.x - trans[0]
          grouped_person_y = trackedPersons.tracks[grouped_person_id].pose.pose.position.y - trans[1]
          grouped_person_distance = math.sqrt(grouped_person_x ** 2 + grouped_person_y ** 2)
          if grouped_person_distance < closed_person_distance:
            closed_person_id = grouped_person_id
            closed_person_distance = grouped_person_distance
        except:          
          continue
      tracked_persons_index[i] = closed_person_id  

  tracked_persons_index_list = tracked_persons_index.tolist()
  num_trackedPersons = len(trackedPersons.tracks)

  for k in range(num_trackedPersons):
    if tracked_persons_index_list.count(k) == 0:
      trackedPersonsFiltered.tracks[k] = 0
   
  tracks_copy = trackedPersonsFiltered.tracks
  tracks_copy = [idx for idx in tracks_copy if not idx == 0]
  trackedPersonsFiltered.tracks = tracks_copy  
  pub.publish(trackedPersonsFiltered)

### Main method
def main():
    rospy.init_node("tracked_persons_filter")   
    trackedPersonsTopic = rospy.resolve_name("/tracked_persons")
    trackedGroupsTopic = rospy.resolve_name("/spencer/perception/tracked_groups")
    trackedPersonsFilteredTopic = rospy.resolve_name("/tracked_persons_filtered")  
    trackedPersonsSubscriber = message_filters.Subscriber(trackedPersonsTopic, TrackedPersons) 
    trackedGroupsSubscriber = message_filters.Subscriber(trackedGroupsTopic, TrackedGroups) 
    timeSynchronizer = message_filters.TimeSynchronizer([trackedPersonsSubscriber, trackedGroupsSubscriber], 100)
    timeSynchronizer.registerCallback(tracked_persons_filter_Callback) 

    global listener
    listener = tf.TransformListener()
    global pub
    pub = rospy.Publisher(trackedPersonsFilteredTopic, TrackedPersons, queue_size=3)    
    rospy.spin()

### Entry point
if __name__ == '__main__':
    main()
