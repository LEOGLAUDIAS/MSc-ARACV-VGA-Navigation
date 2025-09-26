# Assignment
Vision-Guided Autonomous Navigation in ROS

This project implements a vision-guided autonomous navigation system in ROS (Robot Operating System) using OpenCV for image processing.
The robot receives images from an RGB camera, detects a colored target (example: red object), and adjusts its motion commands (/cmd_vel) to follow or align with the object.

Features
* Real-time object detection using color segmentation (HSV space).
* Simple decision-making logic to move the robot:
    Forward if the object is centered.
    Left / Right if the object is off-center.
    Stop if no object is detected.
* ROS-based implementation with image streaming via /camera/rgb/image_raw.
* OpenCV window for debugging and visualization of the camera feed.
