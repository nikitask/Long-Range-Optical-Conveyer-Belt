#Dictionary for HOLO_COMMON common block in idl 
# 9/30/14 Lauren Blackburn converted holo_init.pro from idl to python

class Calibrations():
    def __init__(self, slm = [], doe = [], zoffset = 0.):
       # self.slm_w = 1280.          # width of SLM window (pixels)
        self.slm_w = 1920.
        #self.slm_h = 1024.          # height of SLM window (pixels) 
        self.slm_h = 1080.
        self.slm_gamma = 1.         # gamma of SLM video display channel 
        #self.doe_w = 1280.          # width of computed DOE (pixels)
        self.doe_w = 1920.
        #self.doe_h = 1024.          # height of computed DOE (pixels)
        self.doe_h = 1080.
        #self.xc = 200.             # offset of optical axis relative  . . .
        self.xc = -180.             # offset of optical axis reative . . .      
        #self.yc = -40.             # . . . to center of SLM (pixels)
        self.yc = 60.               #. . . to center of SLM (pixels)
        # NOTE: this is the center for the split screen setup!
        self.xscale = 1.            # ratio of x unit length to y unit
        self.scale = 1.             # conversion of unit length to y unit       
        self.theta = 0.             # orientation of CCD relative to SLM (radians)
        self.zoffset = 0.           # default axial displacement (pixels)
        self.zfactor = 1.           # final zfactor of 1./(lambda * f^2)
        self.ccd_xc = 320.          # location of optical axis . . . 
        self.ccd_yc = 240.          #. . . on the CCD (pixels)                
        self.spherical = 0.         # spherical aberration (wavelengths)
        self.coma = 0.              # coma (wavelengths)
        self.coma_theta = 0.        # orientation of coma (radians)
        self.astig = -0.            # astigmatism (radians)
        self.astig_theta = 0.       # orientation of astigmatism (radians) 
        self.curvature = 0.         # curvature of feild (wavelengths)
        self.distortion = 0.        # barrel distortion (wavelengths)
        self.dis_theta = 0.         # orientation of distortion 
        self.mppslm = 8.            # micrometers per pixel of slm
        self.mppccd = 0.135         # micrometers per pixel of ccd
        self.fobj = 1600.           # focal length objective micrometers
        self.lamba = 0.532          # trapping laser wavelength
        
        if len(slm) > 0:
            self.slm_w = slm[0]
            if len(slm) > 1:
                self.slm_h = slm[1]
            else:
                self.slm_h = slm[0]
        
        if len(doe) > 0:
            self.doe_w = doe[0]
            if len(doe) > 1:
                self.doe_h = doe[1]
            else:
                self.doe_h = doe[0]

        if zoffset != 0:
            self.zoffset = zoffset

    def getparams(self):
        return [self.slm_w, self.slm_h, self.doe_w, self.doe_h, self.zoffset]
