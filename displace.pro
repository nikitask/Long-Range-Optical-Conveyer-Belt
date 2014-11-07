;+
; NAME:
;          displace
;
; PURPOSE:
;          Calculates a phase grating which displaces an optical trap
;          from the center of the field of view to any desired
;          location in three dimensions.  Can be used to displace the
;          traps in a previously calculated HOT DOE.
;
; CATEGORY:
;          Computer-generated holography
;
; CALLING SEQUENCE:
;          phi = offset( dx, dy, [dz] )
;
; INPUTS:
;          dx, dy: in-plane offsets measured in pixels.
;          optionally, dx can be a two- or three-element array
;          containing x, y and z offsets.
; 
; OPTIONAL INPUT:
;          dz: out-of-plane offset in pixels.
;
; OUTPUTS:
;          phi: Real-valued phase grating in the range 0 to 2 pi.
;
; KEYWORDS:
;          nomod: If set, then return phi rather than phi mod 2 pi.
;          
; PROCEDURE:
;          Appropriately scaled plane wave and Fresnel lens.
;
; EXAMPLE:
;          Displace a preexisting phase hologram by 10 pixels in x,
;          -10 pixels in y and 50 pixels in z.
;          
;          IDL> calibrate, ccd, slm
;          IDL> disp = displace( 10, -10, 50, cal = slm )
;          IDL> phi_disp = doe_add( phi, disp )
;          
;
; MODIFICATION HISTORY:
; 2/11/2002: David G. Grier, The University of Chicago.  Created.
; 8/21/2003: DGG added center keyword.
; 9/25/2003  DGG retired CENTER in favor of CAL, calibration constants
;            from CALIBRATE.
; 10/1/2003: DGG added keyword NOMOD.
; 7/20/2004: DGG, New York University.
;            Allow dx to be multidimensional.
; 1/18/2005: DGG. Allow dim to have one or two elements.
; 9/29/2006: DGG. Modified to use HOLO_COMMON for calibration
;     constants.  Removed CAL and DIM keywords
; 9/6/2013 : David Ruffner and Henrique Moyses, changed calculation of 
              ;spatial frequencies to incorporate objective focal length.
;-

function displace, dx, dy, dz, nomod = nomod

common holo_common, cal


;;;;;
; Multiply the z-values by the z-calibration factor (Bhaskar)
;zcalv = 2.1


w = cal.doe_w
h = cal.doe_h
xc = cal.xc
yc = cal.yc
xfac = cal.xscale
rfac = cal.scale
zfac = cal.zfactor

threeD = 0
if n_params() eq 3 then threeD = 1

if n_elements(dx) ge 2 then begin
    dy = dx[1]
    if n_elements(dx) eq 3 then begin
        dz = dx[2]
        threeD = 1
    endif
 endif

thetac = cal.theta
twopi = 2.D * !dpi
kx = ((twopi*cal.mppslm^2)/(cal.lambda*cal.fobj))* $ 
         (dx[0] * cos(thetac) + dy * sin(thetac))* $
         (cal.mppccd/cal.mppslm)
ky = ((twopi*cal.mppslm^2)/(cal.lambda*cal.fobj))* $ 
         (-dx[0] * sin(thetac) + dy * cos(thetac))* $
         (cal.mppccd/cal.mppslm)
if threeD then $
     kz = (twopi  * dz*cal.mppccd*cal.mppslm^2)/ $
                                        (2*cal.lambda*cal.fobj^2)

; coordinates in SLM plane (row vectors)
;print,"xc",xc
;print,"yc",yc

x = xfac * rfac * (dindgen(w) - xc- w/2); Or should it by -(w-1)/2??
x = rebin(x,w,h)
y = rfac * (dindgen(h) - yc -h/2)
y = transpose(rebin(y,h,w))
if threeD then $ 
   rsq = x^2  +  y^2

phi = kx*x+ky*y
if threeD then phi += -kz*rsq

;; a = dindgen(w, h)
;; x = xfac * rfac * ((a mod w) - w/2.D) - xc
;; y = rfac * (floor(a / h) - h/2.D) - yc
;; phi = dx[0] * x / w + dy * y / h
;; if threeD then $
;;     phi = temporary(phi) + zfac * (x^2 + y^2) * dz * zcalv

phi = phi - min(phi)
;phi = 2.D * !dpi * temporary(phi)
;help,phi
if not keyword_set(nomod) then $
  phi = temporary(phi) mod (2.D * !dpi)

return, phi
end
