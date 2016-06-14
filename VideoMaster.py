# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 11:26:07 2016

@author: nikit
"""

import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import pims
import trackpy as tp
import matplotlib.pyplot as plt
import matlab as m
import cv2 as cv
import h5py
import os



def VideotoArray(path):
    video = cv.VideoCapture(path)
    success,image = video.read()
    count = 0
    while success: #comment if frames are already saved
        success,image = video.read()
        cv.imwrite('pic%d.png'% count,image)
        source = '/Users/nikit/Desktop/Tractormaster/pic%d.png'% count
        print(source)
        os.rename('/Users/nikit/Desktop/Tractormaster/pic%d.png'% count,'/Users/nikit/Desktop/Tractormaster/Video2/pic%d.png'%count)
        if cv.waitKey(10)== 27:
            break
        count += 1 
    frames = pims.ImageSequence('/Users/nikit/Desktop/Tractormaster/Video2/pic*.png' ,as_grey=True)    
    return frames

def ImagetoArray(path):
    frames = pims.ImageSequence('/Users/nikit/Desktop/Tractormaster/Video1/pic*.png' ,as_grey=True) 
    crop_frame = []
    c = len(frames)
    for n in range(c-1):
        frame_img = frames[n]
        width, height = frame_img.shape[:2]
        crop_frame += [frame_img[150:400]]
    return crop_frame
    

def Pathcalc(videoarray,start=535,end=540):
    h = h5py.File('myvideofile.hdf4','a')
    print(videoarray)
    f = tp.batch(videoarray[start:end],17,minmass=400)
    t = tp.link_df(f,5,memory=3)
    t.head()
    t1 = tp.filter_stubs(t,3)
    print('After:',t1['particle'].nunique())
    plt.figure()
    tp.mass_size(t1.groupby('particle').mean())
    #tp.plots(frames[0])
    plt.figure()
    tp.plot_traj(t1) 
    plt.show()
    return t1
    
def init_VideotoDataset(array,datasetname): #use if File has not been created
    f = h5py.File('myvideofile.hdf4','a')
    grp = f.create_group("raw video")
    videoarray = grp.create_dataset(datasetname,data=array)
    f.close()
    return videoarray

def VideotoDataset(array,datasetname): #use if file has been created
    f = h5py.File('myvideofile.hdf4','a')
    grp = f.require_group("raw video")
    videoarray = grp.require_dataset(datasetname,data=array,shape = (len(array),250,640),dtype=('uint8'))
    f.close()
    return videoarray
    
def CallDataset(datasetname):
    f = h5py.File('myvideofile.hdf4','a')
    grp = f.require_group("raw video")
    videoarray = grp[datasetname]
    return videoarray
    
def SaveDataset(datasetname,filetitle):
    np.savetxt(str(filetitle),datasetname)
    
    
path = '/Users/nikit/Desktop/Tractormaster/test2.avi'
#frames = VideotoArray(path)
#crop = ImagetoArray(path)
#print(crop)
frames = pims.ImageSequence('/Users/nikit/Desktop/Tractormaster/Video2/pic*.png' ,as_grey=True) 
#videoarray = CallDataset(datasetname = '10-30-15_8')
#print(videoarray)
dance = Pathcalc(frames,150,200)
np.savetxt('test 1',dance)
    
    

    
    

#condition = lambda x: ((x[]))

