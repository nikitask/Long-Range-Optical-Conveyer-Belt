;+
; NAME:
;     holo_init
;
; PURPOSE:
;     Set up the HOLO_COMMON common block for HOT applications.
;
; CATEGORY:
;     Computational holography.  Holographic optical trapping.
;
; CALLING SEQUENCE:
;     holo_init
;
; KEYWORDS:
;     slm: 2-element array containing the width and height of the SLM.
;     doe: 2-element array containing the width and height of the DOE.
;          One element is enough if the two are the same.
;     zoffset: z displacement of trapping plane.
;
; COMMON BLOCKS:
;     HOLO_COMMON
;
; RESTRICTIONS:
;     Should be called before any of the other software in the HOLO
;     suite, preferably from .idlstartx
;
; PROCEDURE:
;     Straightforward
;
; EXAMPLE:
;     IDL> holo_init, slm=[640,480], doe=480, zoffset=-200
;
; MODIFICATION HISTORY:
; 06/05/2006: Written by David G. Grier, New York University
; 09/29/2006: DGG Added ZOFFSET calibration constant and keyword.
;    Added zfactor calibration constant.
; 10/10/2006: DGG.  Commented code.  Added calibration constants for
;    aberration correction.
;
; Copyright (c) 2006 David G. Grier
;-

pro holo_init, slm=slm, doe=doe, zoffset = zoffset,restore=restore,load=load

common holo_common, cal

if n_elements(restore) eq 0 and n_elements(load) eq 0 then begin
  cal = {slm_w:     1920L, $     ; width of SLM window (pixels)
         slm_h:     1080L, $     ; height of SLM window (pixels)
         slm_gamma:   1., $     ; gamma of SLM video display channel
         doe_w:     1920L, $     ; width of computed DOE (pixels)
         doe_h:     1080L, $     ; height of computed DOE (pixels)
         ;xc:          -380., $     ; offset of optical axis relative ...
         ;yc:          100., $     ; ... to center of SLM (pixels)
         xc:          -180., $     ; offset of optical axis relative ...
         yc:          60., $     ; ... to center of SLM (pixels)
         xscale:      1., $     ; ratio of x unit length to y unit.
         scale:       1., $     ; conversion of unit length to CCD pixels
         theta:       0., $     ; orientation of CCD relative to SLM (radians)
         zoffset:     0., $     ; default axial displacement (pixels)
         ;zfactor0:    1.,$    ; intial conversion factor for
                                 ; axial displacements, multiplied by
         zfactor:     1.,$      ; final zfactor
                                  ;;; of 1./(lambda * f^2)
         ccd_xc:    320., $     ; location of of optical axis ...
         ccd_yc:    240., $     ; ... on the CCD (pixels)
         spherical:   0., $     ; spherical aberration (wavelengths)
         coma:        0., $     ; coma (wavelengths)
         coma_theta:  0., $     ; orientation of coma (radians)
         astig:       -0., $     ; astigmatism (radians)
         astig_theta: 0, $     ; orientation of astigmatism (radians)
         curvature:   0., $     ; curvature of field (wavelengths)
         distortion:  0., $     ; barrel distortion (wavelengths)
         dis_theta:   0., $       ; orientation of distortion (radians)
         mppslm:      8.d,$      ;micrometers per pixel of slm
         mppccd:      0.135,$      ;micrometers per pixel of ccd
         fobj:        1600.d, $    ;focal lenght objective micrometers
         lambda:      0.532d }     ;trapping laser wavelength
endif else begin
   if n_elements(load) ne 0 then begin 
      savedcal = load
   endif else savedcal = "calibrations.sav"
   restore,savedcal
endelse

if n_elements(slm) ge 1 then begin
    cal.slm_w = slm[0]
    if n_elements(slm) ge 2 then $
      cal.slm_h = slm[1] $
    else $
      cal.slm_h = cal.slm_w
endif

if n_elements(doe) ge 1 then begin
    cal.doe_w = doe[0]
    if n_elements(doe) ge 2 then $
      cal.doe_h = doe[1] $
    else $
      cal.doe_h = cal.doe_w
endif

if n_elements(zoffset) eq 1 then $
   cal.zoffset = zoffset



end
