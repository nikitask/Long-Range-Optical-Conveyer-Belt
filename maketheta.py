#1/3/14 Lauren Blackburn converted maketheta.pro from idl to python 
import holo_common as common
import numpy as np
import math

def maketheta(x = 0, y = 0, dim = [], cal = [], nocal = []):
    c = common.Calibrations()

    w = c.doe_w
    h = c.doe_h
    if len(dim) > 0:
        w = dim[0]
        if len(dim) > 2:
            h = dim[1]
        else:
            h = w

    if len(nocal) > 0:
        xc = 0.
        yc = 0.
        xfac = 1.
    elif len(cal) >= 2:
        xc = double(cal[0])
        yc = double(cal[1])
        if len(cal) >= 3:
            xfac = double(cal[2])
    else:
        xc = c.xc
        yc = c.yc
        xfac = c.xscale

    rfac = c.scale

    x1d = xfac * rfac * (np.arange(w) - xc - w/2) # or should it be -(w-1)/2 ??
    y1d = rfac * (np.arange(h) - yc - h/2)
    x, y, = np.meshgrid(x1d, y1d)
    theta = np.arctan2(y, x)

    print theta    
    return theta
