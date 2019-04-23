Title: Behavioral cloning
Date: 2019-04-11 00:00
Authors: me
Summary: Convolutional neural network to drive a car!
Template: project_detail
save_as: projects/behavioral-cloning.html
Technologies:python,jupyter,opencv,numpy,keras
Images:projects\cloning.png
repository:https://github.com/tartieret/Self-driving-car---Behavioral-Cloning-
video:https://www.youtube.com/embed/ndFI6WZbOiA

## Project description

In this project, I implemented a deep learning model to learn the correct steering angle for a car, using images taken from a camera at the front of the car.

The goals / steps of this project are the following:

1. Use a simulator to collect data of good driving behavior
2. Build a convolution neural network in Keras that predicts steering angles from images
3. Train and validate the model
4. Test that the model successfully drives around a track without leaving the road

### Model Architecture and Training Strategy

I implemented an architecture defined by NVIDIA as my deep learning model. It consists of a normalization layer, followed by 5 convolution layers, followed by 4 fully connected layers. The model includes RELU layers to introduce nonlinearity and the data is normalized in the model using a Keras lambda layer.

The data was randomly split between training (80%) and cross validation (20%) datasets in order to prevent overfitting. I also trained the model on images coming from the two tracks available in order to help it to generalize.

### Training data

Training data was chosen to keep the vehicle driving on the road. I used the following combination:

- 2 loops of center lane driving
- 1 loop of "reverse" driving
- 1 loop recovering from the left and right sides of the road
- 2 loops of center lane driving with the second track available

To augment the data set, I also flipped images and angles in order to help the model to generalize.

After the collection process, I had 21130 data points, from 3 cameras (left, right, center). Considering the flipping, this gave 84,520 images for training and cross validation. I then preprocessed this data by cropping the top part of the images in order to reduce the image of changing landscape.

### Solution Design Approach

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set.

The first experiments led to a good cross validation error but the car was not driving properly through some of the steep curves. In order to improve the driving behavior, I spent time enhancing the training data set by focusing on curves and recovery from the sides of the road. At first, using images from the left and right side cameras did not improve the driving so I had to optimize the correction factor and find the right value in order to use this additional data and improving the car driving ability.

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road. The end result is shown below:
