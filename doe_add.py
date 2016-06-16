#Written by Nikitas Kanellakopoulos, 11/11/2014
#doe_add2.py 
#Purpose: Combine two phase gratings into one.

import numpy as np
import scipy as sp
import random
def construct(phi1, phi2, nomod = 0, amp1 =[], amp2=[], eta = 0, ampout= 0): #does ampout need to be there?
	if len(amp1) > 0 or len(amp2) > 0:
		tempshape = phi1.shape
		w = tempshape[1]
		h = tempshape[0]
		if len(amp1) == 0:
			temp1 = np.ones(w)
			temp2 = np.ones(h)
			for r in temp2:
				amp1 += [temp1]
		if len(amp2) == 0:
			temp1 = np.ones(w)
			temp2 = np.ones(h)
			for r in temp2:
				amp2 += [temp1]
		psi1 = amp1 * np.exp(1j*phi1)
		psi2 = amp2 * np.exp(1j*phi2)
		psi = psi1 * psi2
		psi = np.array(psi)
		apsi = abs(psi)
		psi = psi/(np.amax(abs(psi)))
		phi = np.arctan2(sp.real(psi),sp.imag(psi))
		phi -= np.amin(phi)
		phi = phi % (2.*np.pi)
		eta = 2*np.median(abs(psi))
		randarray = np.array([[random.random() for i in range(w)] for j in range(h)])
		shape = (abs(psi) >= (eta*randarray)) 
		index = np.where(shape == False)
		phi[index] = 0
		ampout = abs(psi)
	else:
		phi = phi1 + phi2
		phi = phi - np.amin(phi)
		phi = phi % (2.*np.pi)
	return phi
