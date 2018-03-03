#!/usr/bin/env python
__author__  = "Master Computer Vision. Team 02"
__license__ = "M6 Video Analysis. Task 1"

# Import libraries
import os
import math
import cv2
import numpy as np

# Path to save images and videos
images_path = "std-mean-images/"
video_path = "background-subtraction-videos/"


def get_accumulator(path_test):

    """
    Description: get accumulator structure data
    Depends on image size to define borders
    Data are coded into 32 bits of floats
    Input: path test 
    Output: accumulator
    """

    # Initialize accumualtor
    accumulator = np.zeros((0,0), np.float32) 

    # Set accumulator depending on dataset choosen
    if path_test == "datasets/highway/input/":
        accumulator = np.zeros((240,320,150), np.float32)
    if path_test == "datasets/fall/input/":
        accumulator = np.zeros((480,720,50), np.float32)
    if path_test == "datasets/traffic/input/":
        accumulator = np.zeros((240,320,50), np.float32)

    return accumulator


def adaptive(path_test, first_frame, last_frame, mu_matrix, sigma_matrix, alpha, rho):

    """
    Description: background adapts
    Input: path_test, first_frame, last_frame,  mean_matrix, std_matrix, alpha, rho
    Output: None
    """

    # Initialize index to accumulate images
    index = 0

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path+"adaptive_"+str(path_test.split("/")[1])+".avi", fourcc, 60, (get_accumulator(path_test).shape[1], get_accumulator(path_test).shape[0]))

    # Read sequence of images sorted
    for filename in sorted(os.listdir(path_test)):
       
        # Check that frame is into range
        frame_num = int(filename[2:8])
        if frame_num >= first_frame and frame_num <= last_frame:

            # Read image from groundtruth in grayscale
            frame = cv2.imread(path_test+filename, 0)

            # Compute pixels that belongs to background
            background = abs(frame - mu_matrix) >= alpha*(sigma_matrix+2);
            # Convert bool to int values
            background = background.astype(int)
            # Replace 1 by 255
            background[background == 1] = 255
            # Scales, calculates absolute values, and converts the result to 8-bit
            background = cv2.convertScaleAbs(background)
            # Get foreground pixels
            foreground = cv2.bitwise_not(background)

            # Write frame into video
            video_frame = cv2.cvtColor(background, cv2.COLOR_GRAY2RGB)
            out.write(video_frame)	

            # Apply background mask to frame image to retrieve only background grayscale pixels 
            background = cv2.bitwise_and(frame, frame, mask = background)
            # Apply foreground mask to frame image to retrieve only foreground grayscale pixels 
            foreground = cv2.bitwise_and(frame, frame, mask = foreground)

            # Compute mu matrix on all background pixels
            mu_matrix = ((rho*background)+((1-rho)*mu_matrix));
            # Add foreground pixels
            mu_matrix = mu_matrix + foreground
            # Scales, calculates absolute values, and converts the result to 8-bit
            mu_matrix = cv2.convertScaleAbs(mu_matrix)

            # Compute sigma matrix on all background pixels
            sigma_matrix = (rho**pow((background-mu_matrix),2))+((1-rho)**pow(sigma_matrix,2))
            # Add foreground pixels
            sigma_matrix = sigma_matrix + foreground
            # Scales, calculates absolute values, and converts the result to 8-bit
            sigma_matrix = cv2.convertScaleAbs(sigma_matrix)


