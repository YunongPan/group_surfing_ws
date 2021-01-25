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
	  
	*Note: This changes the path only for the current shell. If you want to use your plugin for every new temrinal you open, append the line above to the* `~/.bashrc` *file.*
  
2. Copy human model  
  
	Open `~/group_surfing_ws/src/gazebo_model`. Copy `human_male_1` folder into `~/.gazebo/models`.  
   
3. Start simulation in gazebo  
  
	`cd ~/group_surfing_ws`  
  
	`./run_gazebo.sh`  
  
	*Note: Click on the current shell and use*  
  
	*t	z	u*  
	*g	h	j*  
	*b	n	m*  
  
	*to control the movement of the two human models on the right.*  
  
4. Start another terminal and launch the open source leg tracker, then click back to the terminal of 3. step and try to move the human models toward the goal (default: x = 40.0 m, y = 0.0 m). Group-surfing should be started successfully.
  
	`roslaunch people_velocity_tracker tracked_detector.launch`  
  
	*Note: If the leg tracker is launched together in the same launch file in the 3. step, an error will appear.*  
  
5. Start Rviz  
  
	`cd ~/group_surfing_ws`  
  
	`./run_rviz.sh`
  
6. Control the movement of single human model in the left side  
  
	`roslaunch people_mover human_velocity_publisher.launch`  
  
	*Note: Default velocity: v_x = 0.7 m/s, v_y = 0.0 m/s.*  
	*You may change the velocity in* `~/group_surfing_ws/src/people_mover/launch/human_velocity_publisher.launch`  
	*Press* `ctrl + c` *to stop the movement.*  
  
## Parameter  
  
### The following parameters can be set in `follower.launch`
	Path: `~/group_surfing_ws/src/mybot_follower/launch/follower.launch`  
	#### /mybot_people_tf_broadcaster/goal_x (default: 40.0 m)
#### /mybot_people_tf_broadcaster/goal_y (default: 0.0 m)
#### /mybot_people_tf_broadcaster/max_direction_difference (default: 0.5236 rad)
#### /mybot_people_tf_broadcaster/max_robot_velocity (default: 2.0 m/s)
  
### The following parameters can be set in `human_velocity_publisher.launch`
Path: `~/group_surfing_ws/src/people_mover/launch/human_velocity_publisher.launch`  
#### /human_velocity_publisher/human_left_velocity_x (default: 0.7 m/s)
#### /human_velocity_publisher/human_left_velocity_y (default: 0.0 m/s)

  
![image](https://raw.githubusercontent.com/YunongPan/readme_add_pic/main/group_surfing.png)

