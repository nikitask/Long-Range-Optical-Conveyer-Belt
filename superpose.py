import scipy as sp
import random
import numpy as np

def construct(phi1, phi2, alpha=1, amp1 = [], amp2 = [], ampout = []):
    phi1 = np.array(phi1)
    phi2 = np.array(phi2)
    tempshape = phi1.shape
    w = tempshape[1]
    h = tempshape[0]
    if len(amp1) == 0:
        temp1 = np.ones(w)
        temp2 = np.ones(h)
        for r in temp2:
            amp1 += [temp1]
    if len(amp2) == 0:
        temp1 = ones(w)
        temp2 = ones(h)
        for r in temp2:
            amp2 += [temp1]
    psi = (amp1)*np.exp(1j*phi1) + alpha*(amp2)*np.exp(1j*phi2)
    psi = psi/(np.amax(abs(psi)))
    phi = np.arctan2(sp.real(psi),sp.imag(psi))
    phi -= np.amin(phi)
    phi = phi % (2.*np.pi)
    eta =2*np.median(abs(psi))
    ampout = abs(psi)
    return phi, ampout
