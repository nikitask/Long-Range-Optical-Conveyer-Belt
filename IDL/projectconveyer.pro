;script to project a conveyor beam

;First make the amplitude and phase of each bessel beam

b1 = nolensbesseltrap(30)
b2 = nolensbesseltrap(20)

phi1 = b1[*,*,1]     
phi2 = b2[*,*,1]+!pi
amp1 = b1[*,*,0]
amp2 = b2[*,*,0]

;Then superpose them together
phi = superpose2(phi1,phi2,amp1=amp1,amp2=amp2,ampout=amp)

;Combine with a displace
phiout = doe_add2(phi,displace(140,10),amp1=amp,amp2=1,eta=.2,ampout=ampout)

slm,phiout
plotimage,bytscl(phiout),/iso
