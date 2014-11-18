#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
HOLO_TO_SLM:
This program takes in an array, converts it into an image, and projects it onto a widget.
This program then creates a window onto a secondary display and displays the
 widget on that window.
Finally, this program also creates a menu on the original display that shows the projected image and a "quit" button.

INPUT: an image to main(), which is converted to a qimage and sent to both displays.

WARNING: Make sure to click "quit" on the mini-display that shows up on the primary monitor. If only "x" is clicked, 
the python program will run in terminal indefinitely and terminal must be restarted.

authors: Nikitas Kanellakopoulos  and David Ruffner

References: zetcode.com
 
Modification History:
2014_07_31: Edited by David B. Ruffner, New York University
2014_09_08: Edited by Nikitas Kanellakopoulos, NYU. Added ability to import an
image and project it onto the window created.

"""

import sys
from PyQt4 import QtGui, QtCore
import array_to_image #.array_gen() and .img_gen(array) included
import Image
import imghdr
import qimage2ndarray as q2 #used to conver array to image

class SLMcontrol(QtGui.QWidget):
    
    def __init__(self,image):
        super(SLMcontrol, self).__init__()
        
        self.initUI(image)
        
    def initUI(self,image):               
        
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(300,20) 
        
        self.btn = QtGui.QPushButton('Set Hologram',self)
        self.btn.move(300,70)
        self.btn.clicked.connect(self.showDialog)

        self.lbl = QtGui.QLabel(self)
        self.lbl.move(300,100)

        pic = QtGui.QLabel(self)
        pixmap = QtGui.QPixmap(image)
        pixmap = pixmap.scaledToHeight(200)
        pic.setPixmap(pixmap)
    
        self.setGeometry(300, 400, 450, 200)
        self.setWindowTitle('SLMcontrol') 
        self.center() 
      
    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                              'Enter Hologram:')
        if ok:
            self.lbl.setText(text)
            self.lbl.adjustSize()

    
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

   

def main(image='heart.png'): #default image set to locally stored file
    
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget(QtGui.QApplication.desktop().screen(1)) #projects window onto secondary display
    w.setGeometry(0,0,1920,1080)

    if image == 'heart.png': #converting any non-default array into an image
        converted_image = image
        else converted_image = q2.gray2qimage(image, normalize =  True)
  
    pic = QtGui.QLabel(w) #Picture to be projected on SLM
    pic.setGeometry(0,0,1920,1080)
    img = QtGui.QPixmap(converted_image)
    img = img.scaled(1920, 1080)
    pic.setPixmap(img)
  
    ex = SLMcontrol(converted_image)
    
    w.show()
    ex.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
