;+
; NAME:
;     nolensbesseltrap
;
; PURPOSE:
;     Computes the hologram for a holographic no lens bessel trap.
;
; CATEGORY:
;     Computer-generated holography, holographic optical trapping
;
; CALLING SEQUENCE:
;     IDL> phi = nolensbesseltrap(radius, [ell])
;
; INPUTS:
;     radius: Radius of ring trap (pixels)
;
; OPTIONAL INPUTS:
;     ell: Topological charge of ring trap.
;
; OUTPUTS:
;     phi: Phase hologram, suitable for projection with SLM.
;
; KEYWORDS:
;     shape: Shape function, useful for creating more complicated
;            shape-phase holograms.
;
;     eta: Sets relative efficiency by altering the number of
;          selected pixels in the shape function.  Eta > 1 increases
;          diffraction efficiency at the expense of accuracy.
;          Eta < 1 decreases diffraction efficiency, without improving
;          accuracy beyond eta = 1.  Default: [1].
;
;     alpha: Adjusts proportion of light projected into a given angle.
;          alpha[0,*]: Angle [radians] in the range 0 to 2 pi.
;          alpha[1,*]: Proportion at that angle.
;
; COMMON BLOCKS:
;     holo_common: Uses calibration constants.
;
; RESTRICTIONS:
;     RADIUS should be larger than the natural radius of an optical
;     vortex of topological charge ELL.
;
; PROCEDURE:
;     Shape-phase hologram.  Shape function is useful for projecting
;     cleanest rings, but is not necessary.
;
; EXAMPLE:
; A simple, but effective example:
;     IDL> phi = ringtrap(20,10)        ; compute hologram
;     IDL> plotimage, bytscl(phi), /iso ; take a look at it
;     IDL> plotimage, bytscl(fresnel(phi)), /iso
;     IDL> slm, phi
;
; A more sophisticated example:
;     IDL> ring = ringtrap(20,10,shape=s)
;     IDL> grid = fastphase(10.*grid(10)+150.)
;     IDL> phi = s * ring + (1.-s) * grid
;     IDL> slm, phi
;
; Using ETA:
;     IDL> ring = ringtrap(30,20,eta=2,shape=s)
;     IDL> phi = ring*s + blank() * (1. - s)
;     IDL> slm, phi
;
; MODIFICATION HISTORY:
; 10/1/2006: Written by David G. Grier, New York University.
; 11/29/2006: DGG added ETA keyword.
; 12/1/2006: DGG added ALPHA keyword
; 06/19/2012: David Ruffner added scale factor from calibration constant
;-

function nolensbesseltrap, r, ell, eta = eta, alpha=alpha, shape = shape,$
               blend = blend

common holo_common, c  
  

if n_params() eq 1 then ell = 0.
   
rho = makerho()
 
twopi = 2*!pi
;;;;;;

q = r*(twopi*c.mppslm*c.mppccd)/(c.lambda*c.fobj)
print,"foc length",c.fobj
print,"factor",(twopi*c.mppslm*c.mppccd)/(c.lambda*c.fobj)
b = beselj(q*rho) ;;;IMPORTANT Now the scale is determined by
                                 ;;The calibration. the "factor" relates
                                  ; the slm pixels to the ccd pixels
;
b /= max(abs(b))

b = b+complex(0,0);Make complex

phi = atan(b,/phase)
amp = abs(b)
return,[[[amp]],[[phi]]]
end

;; phi = !pi * (b ge 0.)

;; if ell ne 0 then begin
;;    phi += float(ell) * maketheta()
;;    phi -= min(phi)
;;    phi = phi mod (2.*!pi)
;; endif

;; if n_elements(eta) eq 0 then eta = 0

;; factor = eta
;; if n_elements(alpha) gt 0 then begin
;;     theta = alpha[0,*]
;;     a = alpha[1,*]
;;     a /= mean(a)                ; make sure it's a proportion
;;     beta = maketheta() + !pi
;;     factor = eta - 1. + interpol(a,theta,beta)
;; endif


;; shape = abs(b) ge eta*randomu(seed, c.doe_w, c.doe_h)
;; index = where(shape eq 0) 
;; phi(index) = (displace(150,150))(index)
;; if keyword_set(blend) then phi *= abs(b)

;; return, phi
;; end
