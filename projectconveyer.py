#Written by Nikitas Kanellakopoulos, 11/11/2014
#creates an optical conveyer array, and projects it onto the SLM using holo_to_slm



import holo_to_slm,superpose2,doe_add2,nolensbesseltrap,displace1
import qimage2ndarray as q2

amp1, phi1 = nolensbesseltrap.nolensbesseltrap(30)
amp2, phi2 = nolensbesseltrap.nolensbesseltrap(20)
print(amp1.shape, amp2.shape, phi1.shape, phi2.shape)
phi, ampout = superpose2.superpose2(phi1, phi2, amp1 = amp1, amp2 = amp2)
phi3 = displace1.displace(140,10)
#displace with w = 1080, h = 1920 returns phi.shape(1920,1080)
print("THIS IS PHI", phi.shape, phi3.shape)
phiout = doe_add2.doe_add2(phi,phi3, amp1 = ampout)#removed amp2
holo_to_slm.main(phiout)
