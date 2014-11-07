 NAME:
#   displace
#
#PURPOSE:
#   Calculates a phase grating which displaces an optical trap
#   from the center of the field of view to and desired
#   location in three dimensions. Can be used to displace the 
#   traps in a previously calculated HOT DOE.
#
#CATEGORY:
#   Computer-generated holography
#
#CALLING SEQUENCE:
#   phi = offset(x, y)
#
#INPUTS:
#   x, y: in-plane offsets measured in pixels.
#
#OUTPUTS:
#   phi: Real-valued phase grating in the range 0 to 2 pi.
#
#KEYWORDS:
#   z: out-of-plane offset in pixels. Default: 0.
#   dim: [w, h]: dimensions of phase hologram. Default: [480, 480].
#
#PROCEDURE:
#   Appropriately scaled plane wave and Fresnel lens.
#
#EXAMPLE:
#   Displace a preexisting phase hologram by 10 pixels in x, 
#   -10 pixels in y and 50 pixels in z.
#   python> disp = displacee(10, -10, 50)
# 
#MODIFICATION HISTORY:
#   2/11/2002: David G. Grier, The University of Chicago. Created.
#   9/9/2014: Lauren Blackburn, New York University. Translated to python.
#   9/12/2014: Nikitas Kanellakopoulos, New York University. Debug.



import numpy as np

def displace(dx, dy, dz = 0, dim = np.array([])):
    w = 1920.
    h = 1080.

    y1d = np.arange(h)
    x1d = np.arange(w)
    x,y = np.meshgrid(x1d,y1d)
   
    x += - w/2. #translates from (0,480) to (-240,239)
    y +=  - h/2.
   

    
    phi = (dx * x/w) + (dy * y/h)

    if dz != 0 :
        aperture = 5000.     # 5 mm aperture on lens
        wavelength = 0.532 * x / aperture   # wavelength in pixels at aperture
        na = 1.4                        # numerical aperture
        f = aperture/na              # focal length in pixels 
        phi = phi + ((x^2 + y^2) * dz / wavelength * (f^2))

    phi = phi - np.min(phi)
    phi = 2. * np.pi * phi
    phi = phi % (2. * np.pi)
    print("DISPLACE PHI", phi.shape)
    return (phi)


