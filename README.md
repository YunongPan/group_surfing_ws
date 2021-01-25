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
