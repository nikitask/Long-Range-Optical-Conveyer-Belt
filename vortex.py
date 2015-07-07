import numpy as np
import scipy.special as ss
import scipy as sp
import holo_common as common
import makerho 


def construct(a = 50, x = 512., y = 384.):
	vortex = np.ones((768,1024))
	for c in range(1024):
		for b in range(768):
			if c == x:
				vortex[b, c] = 0
	#		elif c <= x:
	#			vortex[b,c] = (a * np.arctan((b-y)/(c-x))) % 256   
	#		elif b <= y:
	#			vortex[b,c] = (a * np.arctan((b-y)/(c-x))) % 256 
  
			else:
				vortex[b,c] = (256*a*  np.arctan((b-y)/(c-x))/3.14159) % 256     
	phiout = vortex
	return phiout
