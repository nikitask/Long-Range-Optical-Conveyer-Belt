;+
; NAME:
;          doe_add
;
; PURPOSE:
;          Combine two phase gratings into one.
;
; CATEGORY:
;          Computer_generated holography
;
; CALLING SEQUENCE:
;          phi = doe_add( phi1, phi2 )
;
; INPUTS:
;          phi1 : phase hologram
;          phi2 : second phase hologram with same dimensions as first
;
; KEYWORDS:
;          nomod: If set, return phi rather than phi mod 2 pi.
;
; OUTPUTS:
;          phi = phi1 + phi2 : Appropriately offset and modded by 2 pi
;
; PROCEDURE:
;          Straightforward
;
; MODIFICATION HISTORY:
; 2/11/2002: David G. Grier, The University of Chicago. Created.
; 10/1/2003: DGG added keyword NOMOD
;-
function doe_add2, phi1, phi2, nomod = nomod,amp1=amp1,amp2=amp2,eta=eta,$
                           ampout=ampout

if n_elements(amp1) ne 0 or n_elements(amp2) ne 0 then begin
   w = n_elements(phi1[0,*])
   h = n_elements(phi1[*,0])
   if n_elements(amp1) eq 0 then amp1 = fltarr(w,h)+1.
   if n_elements(amp2) eq 0 then amp2 = fltarr(w,h)+1.
   psi1 = amp1*exp(dcomplex(0,phi1))
   psi2 = amp2*exp(dcomplex(0,phi2))
   psi = psi1*psi2
   psi = psi/max(abs(psi))
   phi = atan(psi,/phase)
   phi -= min(phi)
   phi = temporary(phi) mod (2.D*!dpi)
   if n_elements(eta) eq 0 then eta = 0;;;Invalidated FIXME
   eta = 2*median(abs(psi))
   print,"eta",eta
   shape = abs(psi) ge eta*randomu(seed, w, h)
   index = where(shape eq 0) 
   phi(index) = (displace(0,0))(index)
   ampout = abs(psi)
endif else begin
   phi = phi1 + phi2
   phi = phi - min(phi)
   if not keyword_set(nomod) then $
     phi = temporary(phi) mod (2.D * !dpi)
endelse
return, phi
end
