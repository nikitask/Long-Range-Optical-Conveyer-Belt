import numpy as np
import scipy.special as ss
import scipy as sp
import holo_common as common
import makerho 

def besselbeam(r, ell = 0, eta = 1, alpha = 0, shape = 0, blend = 0): 
    #correct inital parameters???
    
    c = common.Calibrations()

    rho = makerho.makerho()

    twopi = 2 * np.pi 

    q = r * (twopi * c.mppslm * c.mppccd)  / (c.lamba * c.fobj)
    print("Focal length" , c.fobj)
    print("factor" , (twopi * c.mppslm * c.mppccd) / (c.lamba * c.fobj))
    b = ss.jn(0,q * rho)    # IMPORTANT: now the scale is determined by the 
                          # calibration. The "factor" relats the slm pixels
                          # to the ccd pixels.
    
    b = b + complex(0, 0)  # make complex
    
    phi = np.arctan2(sp.real(b), sp.imag(b))
    phi = (phi + np.pi) * 255 / twopi

    amp = abs(b)

    return amp, phi
    
amp, phi = nolensbesseltrap(3)
print(amp, phi)