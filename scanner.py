import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui, QtCore
#import projectconveyer
import numpy as np
import qimage2ndarray as q2
import time
import cv2.cv as cv #opencv for taking pictures in camera
import projectconveyor
import planewave
import lens
import os
import re
import vortex

def scanner(text):
	text = list(text)
	hologram = []
	x = []
	y = []
	z = []
	for u in text:
		if u == '(':
			index = text.index(u)
			newtext = text[index+1:]
			break 
		else: 
			x += [u]
			
	x = ''.join(x)
	hologram += [x]
	for v in newtext:
		if v == ')':
			index = newtext.index(v)
			newtext = newtext[index+1:]
			break 
		else:
			y += [v]
	y = ''.join(y)
	hologram += [y]
	for w in newtext:
		if w == '+':
			newtext.remove(w)
			hologram1 = scanner(newtext)
			for a in hologram1:
				hologram += [a]
		else:
			break
	
	return hologram


test = scanner('lens(1.5)+planewave(10)+dispatch(10)')
print(test)
