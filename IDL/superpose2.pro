;+
; NAME:
;       superpose
;
; PURPOSE:
;       Calculates a phase hologram encoding the
;       superposition of the trapping patterns produced by
;       two input phase holograms.
;
; CATEGORY:
;       Computer-generated holography, HOT
;
;
; CALLING SEQUENCE:
;       phi = superpose( phi1, phi2 )
;
; INPUTS:
;       phi1, phi2: phase holograms encoding two distinct trapping patterns.
;
; KEYWORD PARAMETERS:
;
;
; OUTPUTS:
;       phi : Phase hologram encoding superposition.
;
; RESTRICTIONS:
;       phi1 and phi2 must have the same dimensions.
;
; PROCEDURE:
;       Straightforward, with no optimization.
;
; MODIFICATION HISTORY:
; 3/10/2002 David G. Grier, The University of Chicago, Created.
; 10/2/2002 DGG, New York University.  Create positive-definite
; phase masks.  Include relative weights.
; 2/12/2007 DGG, modernize ATAN usage.
;-
function superpose2,  phi1, phi2, alpha,amp1=amp1,amp2=amp2,eta=eta,$
                      ampout=ampout
w = n_elements(phi1[0,*])
h = n_elements(phi2[*,0])
if n_elements(amp1) eq 0 then amp1 = dblarr(w,h)+1.d
if n_elements(amp2) eq 0 then amp2 = dblarr(w,h)+1.d
if n_params() eq 3 then $
   psi = dcomplex(amp1)*exp(dcomplex(0, phi1)) + $
 alpha * dcomplex(amp2)*exp(dcomplex(0, phi2)) $
else $
   psi = dcomplex(amp1)*exp(dcomplex(0, phi1)) + $
         dcomplex(amp2)*exp(dcomplex(0, phi2))
psi = psi/max(abs(psi))
;b = where(abs(psi) lt 1/256.)
phi = atan(psi,/phase)
;phi(b) = 0
phi -= min(phi)
phi = temporary(phi) mod (2.D*!dpi)

if n_elements(eta) eq 0 then eta = 0
;plotimage,bytscl(abs(psi)),/iso


;shape = abs(psi) ge eta*randomu(seed, w, h)
eta = median(abs(psi))
print,"eta",eta
;shape = abs(psi) ge eta*randomu(seed, w, h)
;plotimage,bytscl(shape),/iso

;index = where(shape eq 0) 
;phi(index) = (displace(00,00))(index)

ampout = abs(psi)

return, phi
end
