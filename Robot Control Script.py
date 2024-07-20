from __future__ import print_function
from __future__ import division

import sys
import cv2
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

# Initialize global variables
cx = 0  # X-coordinate of the detected object's center
cy = 0  # Y-coordinate of the detected object's center
pub = None  # Publisher for controlling the robot's movement
rate = None  # Rate at which to send commands (1 Hz)
bridge = None  # CvBridge to convert ROS Image messages to OpenCV images

def callback(data):
    global cx, cy
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
        return

    # Find the ball in the image
    find_ball(cv_image)

    # Move the robot towards the detected object
    move_to_object()

def find_ball(img):
    global cx, cy

    # Convert the image to HSV color space
    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_frame = cv2.resize(hsv_frame, (640, 300))  # Resize the HSV image
    img = cv2.resize(img, (640, 300))              # Resize the original image

    # Define HSV range for detecting the ball
    low_H = 0
    low_S = 100
    low_V = 100
    high_H = 18
    high_S = 255
    high_V = 255

    # Create a mask for the ball color
    mask_frame = cv2.inRange(hsv_frame, (low_H, low_S, low_V), (high_H, high_S, high_V))

    # Find contours in the mask
    contours, hierarchy = cv2.findContours(mask_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    X, Y, W, H = 0, 0, 0, 0

    # Loop through contours to find the largest one
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 30:
            x, y, w, h = cv2.boundingRect(contour)
            if w * h > W * H:
                X, Y, W, H = x, y, w, h

    # Draw a rectangle around the detected ball
    img = cv2.rectangle(img, (X, Y), (X + W, Y + H), (0, 0, 255), 2)
    cx = X + (W / 2.0)  # Update object's center X-coordinate
    cy = Y + (W / 2.0)  # Update object's center Y-coordinate

    print("W=%d" % W)
    print(cx)
    cv2.imshow("window", img)  # Display the image with the rectangle
    cv2.waitKey(3)

def move_to_object():
    global cx
    rot = Twist()  # Create a Twist message for robot's velocity commands
    # Determine the direction to move based on the object's position
    if self.cx == 0:
        text = "searching"
        self.rot.angular.z = 0.1  # Rotate to search for the object
        self.rot.linear.x = 0
    else:
        obj_x = self.cx - 320  # Calculate offset from center of the image
        if -40 <= obj_x <= 40:
            text = "straight"
            self.rot.angular.z = 0  # Move straight
            self.rot.linear.x = 0.1
        elif obj_x > 60:
            text = "Left"
            self.rot.angular.z = -0.1  # Turn left
            self.rot.linear.x = 0
        elif obj_x < -60:
            text = "Right"
            self.rot.angular.z = 0.1  # Turn right
            self.rot.linear.x = 0

    # Publish the velocity command
    pub.publish(rot)
    print(text)

def main():
    global pub, rate, bridge
    rospy.init_node('take_photo', anonymous=False)

    # Initialize the publisher for controlling the robot's movement
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(1)  # Set the rate at which to send commands (1 Hz)
    bridge = CvBridge()   # Initialize the CvBridge to convert ROS Image messages to OpenCV images

    # Subscribe to the camera's image topic
    img_topic = "/camera/rgb/image_raw"
    image_sub = rospy.Subscriber(img_topic, Image, callback)

    # Allow time for the subscription to connect
    rospy.sleep(1)

    # Keep the node running
    rospy.spin()

    # Stop the robot when the node shuts down
    stop()

def stop():
    # Stop the robot
    rot = Twist()
    rot.angular.z = 0
    rot.linear.x = 0
    pub.publish(rot)
    print("Stopped")

if __name__ == '__main__':
    main()
