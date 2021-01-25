# group_surfing_ws
Workshop for group_surfing.

## Requirements
- python-catkin-tools
  - `sudo apt-get install python-catkin-tools`  
    
- teleop_twist_keyboard
  - `sudo apt-get install ros-melodic-teleop-twist-keyboard`

## Installation
1. Clone this repository  
  
	`cd ~`  
  
	`git clone https://github.com/YunongPan/group_surfing_ws.git`  
  
2. Install dependencies  
  
	`cd ~/group_surfing_ws`  
  
	`rosdep install --from-paths src --ignore-src -r -y`  
  
3. Build the workspace  
  
	`catkin_make`  

## Testing
1. Source env setting  
  
	`source ~/group_surfing_ws/devel/setup.bash`  
  
	`export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:~/group_surfing_ws/src/gazebo_plugin/plannar_mover_plugin/build`  
   
2. Start simulation in gazebo  
  
	`cd ~/group_surfing_ws`  
  
	`./run_gazebo.sh`  
  
	*Note: Click on the current terminal and use  
  
	*t	z	u  
	*g	h	j  
	*b	n	m  
  
	*to control the movement of the two human models on the right.  
  
3. Start another terminal and launch the open source leg tracker, then group-surfing should be started successfully.
  
	`roslaunch people_velocity_tracker tracked_detector.launch`  
  
	*Note: If the leg tracker is launched together in the same launch file in the 2. step, an error will appear.  
  
3. Start Rviz  
  
	`./run_rviz.sh`
