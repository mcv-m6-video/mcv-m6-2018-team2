#!/usr/bin/env python
__author__  = "Master Computer Vision. Team 02"
__license__ = "M6 Video Analysis"

# Import libraries
import os
import numpy as np
from gaussian_color import *
from train_color import *
from util import *
from sklearn import metrics

# Highway sequences configuration, range 1050 - 1350
highway_path_in = "datasets/highway/input/"	
highway_path_gt = "datasets/highway/groundtruth/"

# Fall sequences configuration, range 1460 - 1560
fall_path_in = "datasets/fall/input/"  
fall_path_gt = "datasets/fall/groundtruth/"  

# Traffic sequences configuration, range 950 - 1050
traffic_path_in = "datasets/traffic/input/"
traffic_path_gt = "datasets/traffic/groundtruth/"

# Group sequences 
path_tests = [highway_path_in,fall_path_in,traffic_path_in]
path_gts = [highway_path_gt,fall_path_gt,traffic_path_gt]
first_frames = [1050,1460,950]
midle_frames = [1199,1509,999]
last_frames = [1349,1559,1049]

# Define color spaces ['RGB','HSV','YCrCb']
colorSpaces=['RGB','HSV','YCrCb']

# Threshold on gaussian
alphas = np.arange(0,5,0.5)             

# Connectivity to fill holes [4, 8]
connectivity = '4'   

# Pixels of area filltering   
minAreaPixels = 100    

# Define accumulators
FP = np.zeros((3,len(alphas),len(colorSpaces)), np.int)
FN = np.zeros((3,len(alphas),len(colorSpaces)), np.int)
TP = np.zeros((3,len(alphas),len(colorSpaces)), np.int)
TN = np.zeros((3,len(alphas),len(colorSpaces)), np.int)
P = np.zeros((3,len(alphas),len(colorSpaces)), np.float)
R = np.zeros((3,len(alphas),len(colorSpaces)), np.float)
F1 = np.zeros((3,len(alphas),len(colorSpaces)), np.float)

if __name__ == "__main__":

    # Hole filling
    # Post process with hole filling
    # Try different connectivities: 4 and 8
    # Report with AUC & gain for each sequences
    # Provide qualitative interpretation
    
    for cI in range(len(colorSpaces)):
        colorSpace=colorSpaces[cI]
        for dataset in [0,1,2]:
            print "Starting gaussian modelling dataset num: "+str(dataset)+" color space: "+colorSpace+"..."
            for aI in range(len(alphas)):
                alpha=alphas[aI]
                mean_matrix, std_matrix = training_color(path_tests[dataset], first_frames[dataset], midle_frames[dataset], alpha, colorSpace);
                FP[dataset,aI,cI], FN[dataset,aI,cI], TP[dataset,aI,cI], TN[dataset,aI,cI], P[dataset,aI,cI], R[dataset,aI,cI], F1[dataset,aI,cI] = gaussian_color(path_tests[dataset], path_gts[dataset], midle_frames[dataset]+1, last_frames[dataset], mean_matrix, std_matrix, alpha, colorSpace,connectivity, minAreaPixels)
                print "Computed gaussian modelling dataset num: "+str(dataset)+" color space: "+colorSpace+" with alpha: "+str(alpha)
            print "Starting gaussian modelling dataset num: "+str(dataset)+" color space: "+colorSpace+"... done. AUC: "+str(metrics.auc(R[dataset,:,cI],P[dataset,:,cI]))+"\n"

    plt.figure(1)
    for j in np.arange(P.shape[2]):
        for i in np.arange(P.shape[0]):
            plt.plot(alphas,F1[i,:,j],label='F1-Dataset'+str(i)+'_'+colorSpaces[j])
    plt.xlabel('alpha')
    plt.legend()

    plt.figure(2)
    for j in np.arange(P.shape[2]):
        for i in np.arange(P.shape[0]):
            plt.plot(R[i,:,j],P[i,:,j],label='Dataset'+str(i)+'_'+colorSpaces[j]+' - AUC='+str(metrics.auc(R[i,:,j],P[i,:,j])))
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()


