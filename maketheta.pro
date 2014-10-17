;+
; NAME:
;      maketheta
;
; PURPOSE:
;      Creates an array whose values are the angles in radians
;      relative to the x-axis of each pixel in the array.
;
; CATEGORY:
;      Geometry, computed holography
;
; CALLING SEQUENCE:
;      theta = maketheta()
;
; INPUTS:
;      none
;
; KEYWORD PARAMETERS:
;         cal: [xc,yc,xfac] coordinates of optical axis on SLM face
;                 and scale factor for x-coordinate.
;                 Setting this parameter overrides global
;                 calibrations.
;         nocal : if set, ignore CAL and do not use global
;                 calibration constants.
;         dim : one- or two-component specification of the phase-mask's
;               dimensions.  If set, overrides and **overwrites**
;               global calibrations.
;
; OUTPUTS:
;         theta: array of angles around center, in radians
;
; COMMON BLOCKS:
;         HOLO_COMMON:
;         Contains global calibration constants.
;
; PROCEDURE:
;         straightforward: uses atan to calculate angles.
;
; EXAMPLE:
;         theta = maketheta()
;
; MODIFICATION HISTORY:
; 04/22/2004 David G. Grier, New York Universty, created.
; 06/05/2006: DGG. Use calibration constants from HOLO_COMMON.
;    Added NOCAL keyword.
; 11/30/2008: DGG. Optionally return Cartesian coordinates.
;    Addex X and Y keywords.
;
; Copyright (c) 2006 David G. Grier
;-

function maketheta, x = x, y = y, dim = dim, cal = cal, nocal = nocal

common holo_common, c

w = c.doe_w
h = c.doe_h
if n_elements(dim) ge 1 then begin
    w = dim[0]
    if n_elements(dim) eq 2 then $
      h = dim[1] $
    else $
      h = w
    c.doe_w = w
    c.doe_h = h
endif

if keyword_set(nocal) then begin
    xc = 0.
    yc = 0.
    xfac = 1.
endif else if n_elements(cal) ge 2 then begin
    xc = double(cal[0])
    yc = double(cal[1])
    if n_elements(cal) ge 3 then $
      xfac = double(cal[2])
endif else begin
    xc = c.xc
    yc = c.yc
    xfac = c.xscale
endelse
rfac = c.scale

x = xfac * rfac * (dindgen(w) - xc- w/2); Or should it by -(w-1)/2??
x = rebin(x,w,h)
y = rfac * (dindgen(h) - yc -h/2)
y = transpose(rebin(y,h,w))
print, x[1:10,1:10]
print, y[1:10,1:10]
;; x = (findgen(w, h) mod w) - xc -w/2.
;; y = floor(findgen(w, h) / w) - yc -h/2.
;; x = xfac * x ;- xc)
;; y -= yc
 
theta = atan(y, x)

return, theta
end
