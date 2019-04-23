Title: Advanced Lane Finding
Date: 2019-04-11 00:00
Authors: me
Summary: Automatically detect the lane boundaries on the road
Template: project_detail
save_as: projects/lane-finding.html
Technologies:python,jupyter,opencv,numpy
Images:projects\lanes.png
repository:https://github.com/tartieret/Selft-Driving-Car---Advanced-Lane-Finding
video:https://www.youtube.com/embed/1xkANfiyPrM

## Project description

In this project,I wrote a software pipeline to identify lane boundaries in a video from the front of a car.

The goals / steps of this project are the following:

1. Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
2. Apply a distortion correction to raw images.
3. Use color transforms, gradients, etc., to create a thresholded binary image.
4. Apply a perspective transform to rectify binary image ("birds-eye view").
5. Detect lane pixels and fit to find the lane boundary.
6. Determine the curvature of the lane and vehicle position with respect to center.
7. Warp the detected lane boundaries back onto the original image.
8. Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

The full code is available in a [Jupyter notebook](https://github.com/tartieret/Selft-Driving-Car---Advanced-Lane-Finding/blob/master/CarND%20Advanced%20Lane%20Lines.ipynb).

The end result is shown below:
