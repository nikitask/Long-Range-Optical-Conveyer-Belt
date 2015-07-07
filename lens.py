import numpy as np
import scipy.special as ss
import scipy as sp
import holo_common as common
import makerho 


def construct(a = .1, x = 512, y = 384):
	lens = np.ones((768,1024))
	for c in range(1024):
		for b in range(768):
			lens[b,c] = a * ((c - x)**2 + (b - y)**2) % 256     
	phiout = lens
	return phiout
