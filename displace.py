# displace.pro traslated to python by Lauren Blackburn 
# 11/7/14

import holo_common as common
import numpy as np

def displace(dx, dy, dz = 0, nomod = True):
    
    c = common.Calibrations()

    w = c.doe_w
    h = c.doe_h
    xc = c.xc
    yc = c.yc
    xfac = c.xscale
    rfac = c.scale
    zfac = c.zfactor

    threeD = 0
    if dz != 0:
        threeD = 1

    thetac = c.theta
    twopi = 2.0 * np.pi
    kx = ((twopi * c.mppslm**2) / (c.lamba * c.fobj)) * (dx * np.cos(thetac) + dy * sin(thetac)) * (c/mppccd / c.mppslm)
    ky = ((twopi * c.mppslm**2) / (c.lamba * c.fobj)) * (-dx * sin(thetac) + dy*cos(thetac)) * (c.mppccd / c.mppslm)
    
    if threeD == 1:
        kz = (twopi * dz * c.mppccd * c.mppslm**2) / (2 * c.lamba * c.fobj**2)

    x1d = xfac * rfac * (np.arange(w) - xc - w/2) #or should is be -(w-1)/2?
    y1d = rfac * (np.arange(h) - yc - h/2)
    x, y, = np.meshgrid(x1d, y1d)

    if threeD = 1:
        rsq = x^2 + y^2

    phi = kx*x + ky*y
    if threeD = 1:
        phi += -kz*rsq

    phi = phi - min(phi)

    if nomod = False:
        phi = phi % (twopi)

    return phi
