#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
HOLO_TO_SLM:
This program takes in an array, converts it into an image, and projects it onto a widget.
This program then creates a window onto a secondary display and displays the
 widget on that window.
There is a "set hologram" button that takes text input and acts on it. Inputting "phaseshift"
will project an optical conveyor beam at phase shifts (2pi/100)*u, u running from 1-100. After it projects one beam, opencv takes a picture and saves it with the corresponding phaseshift, then the program projects the next beam, and so on.
Finally, this program also creates a menu on the original display that shows the projected image and a "quit" button.

authors: Nikitas Kanellakopoulos  and David Ruffner

References: zetcode.com
 
Modification History:
2014_07_31: Edited by David B. Ruffner, New York University
2014_09_08: Edited by Nikitas Kanellakopoulos, NYU. Added ability to import an
image and project it onto the window created.
2014_12_04: Edited by Nikitas Kanellakopoulos, NYU. Added the ability to type "phaseshift" and run 100 phaseshifts of the optical conveyor beam
2014_12_09: Edited by Nikitas Kanellakopoulos, NYU. Added opencv capabilities to "phaseshift," allowing it to take pictures of each phaseshift
2015_1_21: Edited by Nikitas Kanellakopoulos, NYU. Added the ability to display a static conveyor beam in the drop down menu.

"""

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui, QtCore
#import projectconveyer
import numpy as np
import qimage2ndarray as q2
import time
#import cv2.cv as cv #opencv for taking pictures in camera
import cv2 as cv
import projectconveyor
import planewave
import lens
import os
import re
import vortex
import scanner
import holo_common as common
import rayleighsommerfeld
import besselbeam
from PIL import Image

c = common.Calibrations() #import standard calibrations for SLM - specifically to create the correct size arrays 
		
class ImageChanger(QtGui.QWidget):    #creates a widget for a drop down menu 
    def __init__(self, images, parent=None):
        super(ImageChanger, self).__init__(parent)        

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItems(images)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.comboBox)

class MyWindow(QtGui.QWidget): #creates the window to be populated with widgets
    def __init__(self, images, parent=None):
        super(MyWindow, self).__init__(parent)
        self.label = QtGui.QLabel(self)

        self.imageChanger = ImageChanger(images) #inserts the drop down menu
        self.imageChanger.move(self.imageChanger.pos().y(), self.imageChanger.pos().x() + 100)
        self.imageChanger.show()
        self.imageChanger.comboBox.currentIndexChanged[str].connect(self.changeImage)

        self.setGeometry(300, 400, 850, 400)#x1,y1,x2,y2
        self.setWindowTitle('SLMcontrol') 

        qbtn = QtGui.QPushButton('Quit', self) #inserts "quit" button
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit) # FIXME: Implement a TRY and Finally statement
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(500,20) 
	
        self.lbl = QtGui.QLabel(self) #sets label for input text
        self.btn = QtGui.QPushButton('Set Hologram',self)
        self.btn.move(500,70)
        self.btn.clicked.connect(self.showDialog)
    
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.label)

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                              'Enter Hologram:hologram(#)+hologram(#)')
	       
        if ok: #lists input on the right
            self.lbl.setText(text)
            self.lbl.move(500,125)
            self.lbl.adjustSize() 

        if text == "phaseshift":
            for u in range(100):
                phiout = projectconveyor.construct(u*(2.*np.pi/100.)) #calls projectconveyer to create the optical conveyor array
                img = SLM(phiout) #sends the array to SLM() which projects the array onto the SLM
                pixmap = QtGui.QPixmap(img)
                pixmap = pixmap.scaledToHeight(300)
                self.label.setPixmap(pixmap)#sends the array to the smaller window on the main screen
                print(u*(2.*np.pi/100.))
                QtGui.QApplication.processEvents() #pauses the program to let the image buffer onto the SLM and window
			  
        elif text == "cameratest":
             cv.NamedWindow("camera",1) #starts up opencv
             capture = cv.CaptureFromCAM(1)
             QtGui.QApplication.processEvents()
             img = cv.QueryFrame(capture)
             cv.ShowImage("camera",img)
             cv.SaveImage("cameratest.jpg",img)
        elif text == "video": #captures video
             cap= cv.VideoCapture(0)
             fourcc = cv.cv.CV_FOURCC(*'XVID')
 	     #fourcc = cv.VideoWriter_fourcc(*'XVID')
             out = cv.VideoWriter('output.avi',fourcc,50.0,(640,480)) #fps and resolution
             while (cap.isOpened()):
                 ret, frame = cap.read()
                 if ret==True:
                     frame = cv.flip(frame,0)
                     out.write(frame)
                     cv.imshow('frame',frame)
                     if cv.waitKey(1) & 0xFF == ord('q'):
                         break
                 else:
                     break	
             cap.release()
             #out.release()
             cv.destroyAllWindows()
        elif text == "video1": #captures video inline
             self.playing = True
             cap= cv.VideoCapture(0)
             fourcc = cv.cv.CV_FOURCC(*'XVID')
 	     #fourcc = cv.VideoWriter_fourcc(*'XVID')
             out = cv.VideoWriter('output.avi',fourcc,50.0,(640,480)) #fps and resolution
             while self.playing:
                _, data = cap.read()
                data = cv.cvtColor(data, cv.cv.CV_BGR2RGB)
                qImage = QtGui.QImage(data, data.shape[1], data.shape[0], QtGui.QImage.Format_RGB888)
                self.label.setPixmap(QtGui.QPixmap.fromImage(qImage))
                self.label.adjustSize()
                QtGui.qApp.processEvents()
                time.sleep(0.02) 



        else: #IMPORTANT SECTION HERE ---------------ROBUST TEXT ACCEPTOR----------------------------
            text = text.encode('ascii','ignore')	#converts from unicode to ascii	
            text = text.decode('ascii')
            hologram = scanner.scanner(text)#splits up the input into the individual holograms with their paramaters
	    print(hologram)
            phiout = np.zeros((c.slm_h, c.slm_w))
            for indiv in hologram:				
                for file in os.listdir("/home/nikitas/Desktop/TractorMaster"):#searches main folder
                    if indiv[0] in file:
                        if file.endswith('.py'):
                            a = __import__(indiv[0])#imports the corresponding function
                            if indiv[1] == '':
                                subphiout = a.construct()#default
                            else:
					
                                subphiout = a.construct(*indiv[1])#generates the array
                            phiout += subphiout #adds the arrays, next line imports correction
			    """fix = Image.open("/home/nikitas/Desktop/TractorMaster/correction.bmp")
			    fix = np.array(fix)
			    phiout += fix #adds correction map for SLM(532 nm)
			    print("post1",fix)
			    print("post1 shape", fix.shape)"""
            #phiout = phiout.astype(float)
	    #phiout *= 200./256.
	    #phiout = phiout % 256
	    print("post2", phiout)
	    print("post2 shape",phiout.shape)
            converted_image = q2.gray2qimage(phiout, normalize =  True)
            pixmap = QtGui.QPixmap(converted_image)
            pixmap = pixmap.scaledToHeight(300)
            SLM(converted_image)
            self.label.setPixmap(pixmap)
					 
     
    def changeImage(self, pathToImage): #Allows user to cycle through various beam setups
        if pathToImage.endswith('planewave.npy'): #converting any non-default array into an image
                phiout = planewave.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        elif pathToImage.endswith('lens.npy'): #converting any non-default array into an image
                phiout = lens.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        elif pathToImage.endswith('besselbeam.npy'):
            amp, phiout = besselbeam.construct(10)
            converted_image = q2.gray2qimage(phiout, normalize = True)
        elif pathToImage.endswith('conveyorarray.npy'): #converting any non-default array into an image
		x = np.linspace(0,2*np.pi,20)
		for i in range(0,10):
			for u in x:
            			phiout = projectconveyor.construct(u)
                		# testing rayleighsommerfeld 11/9
            			phiout = rayleighsommerfeld.rayleighsommerfeld(phiout, -10.)
            			#phiout *= np.conjugate(phiout)      #take real part from RS??
            			converted_image = q2.gray2qimage(phiout, normalize =  True)
				pixmap = QtGui.QPixmap(converted_image)
       				pixmap = pixmap.scaledToHeight(300)
        			SLM(converted_image)
   				self.label.setPixmap(pixmap)
				QtGui.QApplication.processEvents() #pauses the program to let the image buffer onto the SLM and window
	elif pathToImage.endswith('besselplane.npy'):
		amp,phiout = besselbeam.construct(1)
                # testing rayleighsommerfeld 11/9
            	phiout = rayleighsommerfeld.rayleighsommerfeld(phiout, +50)
            	#phiout *= np.conjugate(phiout)      #take real part from RS??
            	converted_image = q2.gray2qimage(phiout, normalize =  True)
		pixmap = QtGui.QPixmap(converted_image)
       		pixmap = pixmap.scaledToHeight(300)
        	SLM(converted_image)
   		self.label.setPixmap(pixmap)
		QtGui.QApplication.processEvents()
			
        elif pathToImage.endswith('vortex.npy'): #converting any non-default array into an image
                phiout = vortex.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        else: converted_image = pathToImage
        pixmap = QtGui.QPixmap(converted_image)
        pixmap = pixmap.scaledToHeight(300)
        SLM(converted_image)
        self.label.setPixmap(pixmap)



def SLM(array='heart.png'): #default image set to locally stored file
    w = QtGui.QWidget(QtGui.QApplication.desktop().screen(1)) #!!!!!!!!!projects window onto secondary display
    w.setGeometry(0,0,c.slm_w,c.slm_h) #geometry dependent on SLM
    pic = QtGui.QLabel(w) #Picture to be projected on SLM
    pic.setGeometry(0,0,c.slm_w,c.slm_h)
    img = QtGui.QPixmap(array) #convert image to format that can be projected
    img = img.scaled(c.slm_w,c.slm_h)
    pic.setPixmap(img)
    w.show()
    return img

if __name__ == "__main__":
    import sys

    images = [  "heart.png","star.png","besselbeam.npy", "conveyorarray.npy","planewave.npy", "lens.npy", "vortex.npy","besselplane.npy"]
#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
HOLO_TO_SLM:
This program takes in an array, converts it into an image, and projects it onto a widget.
This program then creates a window onto a secondary display and displays the
 widget on that window.
There is a "set hologram" button that takes text input and acts on it. Inputting "phaseshift"
will project an optical conveyor beam at phase shifts (2pi/100)*u, u running from 1-100. After it projects one beam, opencv takes a picture and saves it with the corresponding phaseshift, then the program projects the next beam, and so on.
Finally, this program also creates a menu on the original display that shows the projected image and a "quit" button.

authors: Nikitas Kanellakopoulos  and David Ruffner

References: zetcode.com
 
Modification History:
2014_07_31: Edited by David B. Ruffner, New York University
2014_09_08: Edited by Nikitas Kanellakopoulos, NYU. Added ability to import an
image and project it onto the window created.
2014_12_04: Edited by Nikitas Kanellakopoulos, NYU. Added the ability to type "phaseshift" and run 100 phaseshifts of the optical conveyor beam
2014_12_09: Edited by Nikitas Kanellakopoulos, NYU. Added opencv capabilities to "phaseshift," allowing it to take pictures of each phaseshift
2015_1_21: Edited by Nikitas Kanellakopoulos, NYU. Added the ability to display a static conveyor beam in the drop down menu.

"""

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui, QtCore
#import projectconveyer
import numpy as np
import qimage2ndarray as q2
import time
#import cv2.cv as cv #opencv for taking pictures in camera
import cv2 as cv
import projectconveyor
import planewave
import lens
import os
import re
import vortex
import scanner
import holo_common as common
import rayleighsommerfeld
import besselbeam
from PIL import Image

c = common.Calibrations() #import standard calibrations for SLM - specifically to create the correct size arrays 
		
class ImageChanger(QtGui.QWidget):    #creates a widget for a drop down menu 
    def __init__(self, images, parent=None):
        super(ImageChanger, self).__init__(parent)        

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItems(images)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.comboBox)

class MyWindow(QtGui.QWidget): #creates the window to be populated with widgets
    def __init__(self, images, parent=None):
        super(MyWindow, self).__init__(parent)
        self.label = QtGui.QLabel(self)

        self.imageChanger = ImageChanger(images) #inserts the drop down menu
        self.imageChanger.move(self.imageChanger.pos().y(), self.imageChanger.pos().x() + 100)
        self.imageChanger.show()
        self.imageChanger.comboBox.currentIndexChanged[str].connect(self.changeImage)

        self.setGeometry(300, 400, 850, 400)#x1,y1,x2,y2
        self.setWindowTitle('SLMcontrol') 

        qbtn = QtGui.QPushButton('Quit', self) #inserts "quit" button
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit) # FIXME: Implement a TRY and Finally statement
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(500,20) 
	
        self.lbl = QtGui.QLabel(self) #sets label for input text
        self.btn = QtGui.QPushButton('Set Hologram',self)
        self.btn.move(500,70)
        self.btn.clicked.connect(self.showDialog)
    
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.label)

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                              'Enter Hologram:hologram(#)+hologram(#)')
	       
        if ok: #lists input on the right
            self.lbl.setText(text)
            self.lbl.move(500,125)
            self.lbl.adjustSize() 

        if text == "phaseshift":
            for u in range(100):
                phiout = projectconveyor.construct(u*(2.*np.pi/100.)) #calls projectconveyer to create the optical conveyor array
                img = SLM(phiout) #sends the array to SLM() which projects the array onto the SLM
                pixmap = QtGui.QPixmap(img)
                pixmap = pixmap.scaledToHeight(300)
                self.label.setPixmap(pixmap)#sends the array to the smaller window on the main screen
                print(u*(2.*np.pi/100.))
                QtGui.QApplication.processEvents() #pauses the program to let the image buffer onto the SLM and window
			  
        elif text == "cameratest":
             cv.NamedWindow("camera",1) #starts up opencv
             capture = cv.CaptureFromCAM(1)
             QtGui.QApplication.processEvents()
             img = cv.QueryFrame(capture)
             cv.ShowImage("camera",img)
             cv.SaveImage("cameratest.jpg",img)
        elif text == "video": #captures video
             cap= cv.VideoCapture(0)
             fourcc = cv.cv.CV_FOURCC(*'XVID')
 	     #fourcc = cv.VideoWriter_fourcc(*'XVID')
             out = cv.VideoWriter('output.avi',fourcc,50.0,(640,480)) #fps and resolution
             while (cap.isOpened()):
                 ret, frame = cap.read()
                 if ret==True:
                     frame = cv.flip(frame,0)
                     out.write(frame)
                     cv.imshow('frame',frame)
                     if cv.waitKey(1) & 0xFF == ord('q'):
                         break
                 else:
                     break	
             cap.release()
             #out.release()
             cv.destroyAllWindows()
        elif text == "video1": #captures video inline
             self.playing = True
             cap= cv.VideoCapture(0)
             fourcc = cv.cv.CV_FOURCC(*'XVID')
 	     #fourcc = cv.VideoWriter_fourcc(*'XVID')
             out = cv.VideoWriter('output.avi',fourcc,50.0,(640,480)) #fps and resolution
             while self.playing:
                _, data = cap.read()
                data = cv.cvtColor(data, cv.cv.CV_BGR2RGB)
                qImage = QtGui.QImage(data, data.shape[1], data.shape[0], QtGui.QImage.Format_RGB888)
                self.label.setPixmap(QtGui.QPixmap.fromImage(qImage))
                self.label.adjustSize()
                QtGui.qApp.processEvents()
                time.sleep(0.02) 



        else: #IMPORTANT SECTION HERE ---------------ROBUST TEXT ACCEPTOR----------------------------
            text = text.encode('ascii','ignore')	#converts from unicode to ascii	
            text = text.decode('ascii')
            hologram = scanner.scanner(text)#splits up the input into the individual holograms with their paramaters
	    print(hologram)
            phiout = np.zeros((c.slm_h, c.slm_w))
            for indiv in hologram:				
                for file in os.listdir("/home/nikitas/Desktop/TractorMaster"):#searches main folder
                    if indiv[0] in file:
                        if file.endswith('.py'):
                            a = __import__(indiv[0])#imports the corresponding function
                            if indiv[1] == '':
                                subphiout = a.construct()#default
                            else:
					
                                subphiout = a.construct(*indiv[1])#generates the array
                            phiout += subphiout #adds the arrays, next line imports correction
			    """fix = Image.open("/home/nikitas/Desktop/TractorMaster/correction.bmp")
			    fix = np.array(fix)
			    phiout += fix #adds correction map for SLM(532 nm)
			    print("post1",fix)
			    print("post1 shape", fix.shape)"""
            #phiout = phiout.astype(float)
	    #phiout *= 200./256.
	    #phiout = phiout % 256
	    print("post2", phiout)
	    print("post2 shape",phiout.shape)
            converted_image = q2.gray2qimage(phiout, normalize =  True)
            pixmap = QtGui.QPixmap(converted_image)
            pixmap = pixmap.scaledToHeight(300)
            SLM(converted_image)
            self.label.setPixmap(pixmap)
					 
     
    def changeImage(self, pathToImage): #Allows user to cycle through various beam setups
        if pathToImage.endswith('planewave.npy'): #converting any non-default array into an image
                phiout = planewave.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        elif pathToImage.endswith('lens.npy'): #converting any non-default array into an image
                phiout = lens.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        elif pathToImage.endswith('besselbeam.npy'):
            amp, phiout = besselbeam.construct(10)
            converted_image = q2.gray2qimage(phiout, normalize = True)
        elif pathToImage.endswith('conveyorarray.npy'): #converting any non-default array into an image
		x = np.linspace(0,2*np.pi,20)
		for i in range(0,10):
			for u in x:
            			phiout = projectconveyor.construct(u)
                		# testing rayleighsommerfeld 11/9
            			phiout = rayleighsommerfeld.rayleighsommerfeld(phiout, -10.)
            			#phiout *= np.conjugate(phiout)      #take real part from RS??
            			converted_image = q2.gray2qimage(phiout, normalize =  True)
				pixmap = QtGui.QPixmap(converted_image)
       				pixmap = pixmap.scaledToHeight(300)
        			SLM(converted_image)
   				self.label.setPixmap(pixmap)
				QtGui.QApplication.processEvents() #pauses the program to let the image buffer onto the SLM and window
	elif pathToImage.endswith('besselplane.npy'):
		amp,phiout = besselbeam.construct(1)
                # testing rayleighsommerfeld 11/9
            	phiout = rayleighsommerfeld.rayleighsommerfeld(phiout, +50)
            	#phiout *= np.conjugate(phiout)      #take real part from RS??
            	converted_image = q2.gray2qimage(phiout, normalize =  True)
		pixmap = QtGui.QPixmap(converted_image)
       		pixmap = pixmap.scaledToHeight(300)
        	SLM(converted_image)
   		self.label.setPixmap(pixmap)
		QtGui.QApplication.processEvents()
			
        elif pathToImage.endswith('vortex.npy'): #converting any non-default array into an image
                phiout = vortex.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        else: converted_image#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
HOLO_TO_SLM:
This program takes in an array, converts it into an image, and projects it onto a widget.
This program then creates a window onto a secondary display and displays the
 widget on that window.
There is a "set hologram" button that takes text input and acts on it. Inputting "phaseshift"
will project an optical conveyor beam at phase shifts (2pi/100)*u, u running from 1-100. After it projects one beam, opencv takes a picture and saves it with the corresponding phaseshift, then the program projects the next beam, and so on.
Finally, this program also creates a menu on the original display that shows the projected image and a "quit" button.

authors: Nikitas Kanellakopoulos  and David Ruffner

References: zetcode.com
 
Modification History:
2014_07_31: Edited by David B. Ruffner, New York University
2014_09_08: Edited by Nikitas Kanellakopoulos, NYU. Added ability to import an
image and project it onto the window created.
2014_12_04: Edited by Nikitas Kanellakopoulos, NYU. Added the ability to type "phaseshift" and run 100 phaseshifts of the optical conveyor beam
2014_12_09: Edited by Nikitas Kanellakopoulos, NYU. Added opencv capabilities to "phaseshift," allowing it to take pictures of each phaseshift
2015_1_21: Edited by Nikitas Kanellakopoulos, NYU. Added the ability to display a static conveyor beam in the drop down menu.

"""

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4 import QtGui, QtCore
#import projectconveyer
import numpy as np
import qimage2ndarray as q2
import time
#import cv2.cv as cv #opencv for taking pictures in camera
import cv2 as cv
import projectconveyor
import planewave
import lens
import os
import re
import vortex
import scanner
import holo_common as common
import rayleighsommerfeld
import besselbeam
from PIL import Image

c = common.Calibrations() #import standard calibrations for SLM - specifically to create the correct size arrays 
		
class ImageChanger(QtGui.QWidget):    #creates a widget for a drop down menu 
    def __init__(self, images, parent=None):
        super(ImageChanger, self).__init__(parent)        

        self.comboBox = QtGui.QComboBox(self)
        self.comboBox.addItems(images)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.comboBox)

class MyWindow(QtGui.QWidget): #creates the window to be populated with widgets
    def __init__(self, images, parent=None):
        super(MyWindow, self).__init__(parent)
        self.label = QtGui.QLabel(self)

        self.imageChanger = ImageChanger(images) #inserts the drop down menu
        self.imageChanger.move(self.imageChanger.pos().y(), self.imageChanger.pos().x() + 100)
        self.imageChanger.show()
        self.imageChanger.comboBox.currentIndexChanged[str].connect(self.changeImage)

        self.setGeometry(300, 400, 850, 400)#x1,y1,x2,y2
        self.setWindowTitle('SLMcontrol') 

        qbtn = QtGui.QPushButton('Quit', self) #inserts "quit" button
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit) # FIXME: Implement a TRY and Finally statement
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(500,20) 
	
        self.lbl = QtGui.QLabel(self) #sets label for input text
        self.btn = QtGui.QPushButton('Set Hologram',self)
        self.btn.move(500,70)
        self.btn.clicked.connect(self.showDialog)
    
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.label)

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                              'Enter Hologram:hologram(#)+hologram(#)')
	       
        if ok: #lists input on the right
            self.lbl.setText(text)
            self.lbl.move(500,125)
            self.lbl.adjustSize() 

        if text == "phaseshift":
            for u in range(100):
                phiout = projectconveyor.construct(u*(2.*np.pi/100.)) #calls projectconveyer to create the optical conveyor array
                img = SLM(phiout) #sends the array to SLM() which projects the array onto the SLM
                pixmap = QtGui.QPixmap(img)
                pixmap = pixmap.scaledToHeight(300)
                self.label.setPixmap(pixmap)#sends the array to the smaller window on the main screen
                print(u*(2.*np.pi/100.))
                QtGui.QApplication.processEvents() #pauses the program to let the image buffer onto the SLM and window
			  
        elif text == "cameratest":
             cv.NamedWindow("camera",1) #starts up opencv
             capture = cv.CaptureFromCAM(1)
             QtGui.QApplication.processEvents()
             img = cv.QueryFrame(capture)
             cv.ShowImage("camera",img)
             cv.SaveImage("cameratest.jpg",img)
        elif text == "video": #captures video
             cap= cv.VideoCapture(0)
             fourcc = cv.cv.CV_FOURCC(*'XVID')
 	     #fourcc = cv.VideoWriter_fourcc(*'XVID')
             out = cv.VideoWriter('output.avi',fourcc,50.0,(640,480)) #fps and resolution
             while (cap.isOpened()):
                 ret, frame = cap.read()
                 if ret==True:
                     frame = cv.flip(frame,0)
                     out.write(frame)
                     cv.imshow('frame',frame)
                     if cv.waitKey(1) & 0xFF == ord('q'):
                         break
                 else:
                     break	
             cap.release()
             #out.release()
             cv.destroyAllWindows()
        elif text == "video1": #captures video inline
             self.playing = True
             cap= cv.VideoCapture(0)
             fourcc = cv.cv.CV_FOURCC(*'XVID')
 	     #fourcc = cv.VideoWriter_fourcc(*'XVID')
             out = cv.VideoWriter('output.avi',fourcc,50.0,(640,480)) #fps and resolution
             while self.playing:
                _, data = cap.read()
                data = cv.cvtColor(data, cv.cv.CV_BGR2RGB)
                qImage = QtGui.QImage(data, data.shape[1], data.shape[0], QtGui.QImage.Format_RGB888)
                self.label.setPixmap(QtGui.QPixmap.fromImage(qImage))
                self.label.adjustSize()
                QtGui.qApp.processEvents()
                time.sleep(0.02) 



        else: #IMPORTANT SECTION HERE ---------------ROBUST TEXT ACCEPTOR----------------------------
            text = text.encode('ascii','ignore')	#converts from unicode to ascii	
            text = text.decode('ascii')
            hologram = scanner.scanner(text)#splits up the input into the individual holograms with their paramaters
	    print(hologram)
            phiout = np.zeros((c.slm_h, c.slm_w))
            for indiv in hologram:				
                for file in os.listdir("/home/nikitas/Desktop/TractorMaster"):#searches main folder
                    if indiv[0] in file:
                        if file.endswith('.py'):
                            a = __import__(indiv[0])#imports the corresponding function
                            if indiv[1] == '':
                                subphiout = a.construct()#default
                            else:
					
                                subphiout = a.construct(*indiv[1])#generates the array
                            phiout += subphiout #adds the arrays, next line imports correction
			    """fix = Image.open("/home/nikitas/Desktop/TractorMaster/correction.bmp")
			    fix = np.array(fix)
			    phiout += fix #adds correction map for SLM(532 nm)
			    print("post1",fix)
			    print("post1 shape", fix.shape)"""
            #phiout = phiout.astype(float)
	    #phiout *= 200./256.
	    #phiout = phiout % 256
	    print("post2", phiout)
	    print("post2 shape",phiout.shape)
            converted_image = q2.gray2qimage(phiout, normalize =  True)
            pixmap = QtGui.QPixmap(converted_image)
            pixmap = pixmap.scaledToHeight(300)
            SLM(converted_image)
            self.label.setPixmap(pixmap)
					 
     
    def changeImage(self, pathToImage): #Allows user to cycle through various beam setups
        if pathToImage.endswith('planewave.npy'): #converting any non-default array into an image
                phiout = planewave.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        elif pathToImage.endswith('lens.npy'): #converting any non-default array into an image
                phiout = lens.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        elif pathToImage.endswith('besselbeam.npy'):
            amp, phiout = besselbeam.construct(10)
            converted_image = q2.gray2qimage(phiout, normalize = True)
        elif pathToImage.endswith('conveyorarray.npy'): #converting any non-default array into an image
		x = np.linspace(0,2*np.pi,20)
		for i in range(0,10):
			for u in x:
            			phiout = projectconveyor.construct(u)
                		# testing rayleighsommerfeld 11/9
            			phiout = rayleighsommerfeld.rayleighsommerfeld(phiout, -10.)
            			#phiout *= np.conjugate(phiout)      #take real part from RS??
            			converted_image = q2.gray2qimage(phiout, normalize =  True)
				pixmap = QtGui.QPixmap(converted_image)
       				pixmap = pixmap.scaledToHeight(300)
        			SLM(converted_image)
   				self.label.setPixmap(pixmap)
				QtGui.QApplication.processEvents() #pauses the program to let the image buffer onto the SLM and window
	elif pathToImage.endswith('besselplane.npy'):
		amp,phiout = besselbeam.construct(1)
                # testing rayleighsommerfeld 11/9
            	phiout = rayleighsommerfeld.rayleighsommerfeld(phiout, +50)
            	#phiout *= np.conjugate(phiout)      #take real part from RS??
            	converted_image = q2.gray2qimage(phiout, normalize =  True)
		pixmap = QtGui.QPixmap(converted_image)
       		pixmap = pixmap.scaledToHeight(300)
        	SLM(converted_image)
   		self.label.setPixmap(pixmap)
		QtGui.QApplication.processEvents()
			
        elif pathToImage.endswith('vortex.npy'): #converting any non-default array into an image
                phiout = vortex.construct()
                converted_image = q2.gray2qimage(phiout, normalize =  True)
        else: converted_image = pathToImage
        pixmap = QtGui.QPixmap(converted_image)
        pixmap = pixmap.scaledToHeight(300)
        SLM(converted_image)
        self.label.setPixmap(pixmap)



def SLM(array='heart.png'): #default image set to locally stored file
    w = QtGui.QWidget(QtGui.QApplication.desktop().screen(1)) #!!!!!!!!!projects window onto secondary display
    w.setGeometry(0,0,c.slm_w,c.slm_h) #geometry dependent on SLM
    pic = QtGui.QLabel(w) #Picture to be projected on SLM
    pic.setGeometry(0,0,c.slm_w,c.slm_h)
    img = QtGui.QPixmap(array) #convert image to format that can be projected
    img = img.scaled(c.slm_w,c.slm_h)
    pic.setPixmap(img)
    w.show()
    return img

if __name__ == "__main__":
    import sys

    images = [  "heart.png","star.png","besselbeam.npy", "conveyorarray.npy","planewave.npy", "lens.npy", "vortex.npy","besselplane.npy"]

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
 
    main = MyWindow(images)
    main.show()
   
    

    sys.exit(app.exec_())
 = pathToImage
        pixmap = QtGui.QPixmap(converted_image)
        pixmap = pixmap.scaledToHeight(300)
        SLM(converted_image)
        self.label.setPixmap(pixmap)



def SLM(array='heart.png'): #default image set to locally stored file
    w = QtGui.QWidget(QtGui.QApplication.desktop().screen(1)) #!!!!!!!!!projects window onto secondary display
    w.setGeometry(0,0,c.slm_w,c.slm_h) #geometry dependent on SLM
    pic = QtGui.QLabel(w) #Picture to be projected on SLM
    pic.setGeometry(0,0,c.slm_w,c.slm_h)
    img = QtGui.QPixmap(array) #convert image to format that can be projected
    img = img.scaled(c.slm_w,c.slm_h)
    pic.setPixmap(img)
    w.show()
    return img

if __name__ == "__main__":
    import sys

    images = [  "heart.png","star.png","besselbeam.npy", "conveyorarray.npy","planewave.npy", "lens.npy", "vortex.npy","besselplane.npy"]

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
 
    main = MyWindow(images)
    main.show()
   
    

    sys.exit(app.exec_())

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
 
    main = MyWindow(images)
    main.show()
   
    

    sys.exit(app.exec_())
