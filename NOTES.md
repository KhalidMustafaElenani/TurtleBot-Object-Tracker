# Setup and Execution Notes

## Dependencies
- ROS (Robot Operating System)
- OpenCV
- CvBridge
- rospy
- std_msgs
- sensor_msgs
- geometry_msgs

## Setup Instructions

1. **Start ROS Core:**
   `roscore`
2. Launch Vision Nodes:
   `roslaunch rchomeedu_vision multi_astra.launch`
   `roslaunch robot_vision_openvino yolo_ros.launch`
3. Launch Robot Nodes:
  `roslaunch jupiterobot_bringup jupiterobot_bringup.launch`
4. Run the Robot Control Script:
   `python Main.py`

## Notes
* Ensure ROS and required packages are installed.
* Verify the correct camera topics are being used.
* Adjust HSV ranges in find_ball function based on the object's color.
* Troubleshooting
* If the robot does not move as expected, check the ROS topics and verify that the image processing parameters match the object's characteristics.
* Review ROS and OpenCV logs for any error messages.

