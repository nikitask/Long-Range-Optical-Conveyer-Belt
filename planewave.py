import numpy as np
import scipy.special as ss
import scipy as sp
import holo_common as common
import makerho 


def construct(a = 5):
	x = np.ones((768,1024))
	for c in range(1024):
		for b in range(768):
			x[b,c] =a*c % 256  
	phiout = x
	
	return phiout
