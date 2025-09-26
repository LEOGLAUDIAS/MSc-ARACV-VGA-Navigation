#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist

# Initialize cv_bridge and publisher
bridge = CvBridge()
cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def move_robot(direction):
    
    " Simple movement logic based on object position. Publishes velocity commands to /cmd_vel."
    
    twist = Twist()
    if direction == 'forward':
        twist.linear.x = 0.2   # move straight
    elif direction == 'left':
        twist.angular.z = 0.2  # rotate left
    elif direction == 'right':
        twist.angular.z = -0.2 # rotate right
    else:
        twist.linear.x = 0.0   # stop
        twist.angular.z = 0.0
    cmd_pub.publish(twist)

def image_callback(msg):
    
    "Processes incoming images from the RGB camera, detects the target color, and decides movement."
    
    # Convert ROS Image to OpenCV format
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

    # Convert BGR to HSV
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    # Define color range (example: red cube)
    lower = np.array([0, 120, 70])
    upper = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    direction = 'stop'

    if contours:
        # Select the largest contour
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cx = x + w // 2
        img_center = cv_image.shape[1] // 2

        # Decide movement
        if cx < img_center - 50:
            direction = 'left'
        elif cx > img_center + 50:
            direction = 'right'
        else:
            direction = 'forward'

    move_robot(direction)

    # Debugging window
    cv2.imshow("Camera Feed", cv_image)
    cv2.waitKey(1)

def main():
    rospy.init_node('vision_nav')
    rospy.Subscriber("/camera/rgb/image_raw", Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()
