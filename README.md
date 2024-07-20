## TurtleBot Object Tracker
This script utilizes ROS (Robot Operating System) to autonomously detect and move towards a specific colored object, such as a ball, using computer vision techniques. The TakePhoto class handles image acquisition from the robot's camera, processes the images to identify the target object, and commands the robot to navigate towards it. This implementation is designed specifically for the TurtleBot robot platform.

## TurtleBot
<p align="center">
  <img src="TurtleBot2.jpg" alt="TurtleBot 2" />
</p>

## Key Features:
* Image Processing: Converts ROS image messages to OpenCV format for processing.
* Object Detection: Identifies a red-colored ball using HSV color space and contour detection.
* Autonomous Navigation: Commands the robot to move towards the detected object, adjusting its path based on the object's position.
* ROS Integration: Subscribes to camera image topics and publishes velocity commands to control the robot's movement.

This script is designed for robust and real-time object detection and navigation on the TurtleBot, making it suitable for applications in robotics and automation where autonomous movement towards a target is required.
