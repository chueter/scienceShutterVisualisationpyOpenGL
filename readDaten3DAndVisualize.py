#
#  readDaten3DAndVisualize.py
#  
#
#  Created by Claas Hueter on 1/10/11.
#  Copyright (c) 2011 __MyCompanyName__. All rights reserved.
#
from sys import argv, exit
from re import *
import datetime

#try:
	#from OpenGL.GLUT import *
	#from OpenGL.GL import *
	#from OpenGL.GLU import *
	
#except:
	#print ''' OpenGL not properly installed '''
	#sys.exit( )
	
try:
	re_n = compile('\n') ### re includes only break 
	re_whitespace = compile('\s')  ### re includes whitespaces \t \n \r \f \v
except:
	print ''' could not define regular expression '''
	
try:
	daten3D = file('daten3D.txt', 'r')
	daten3DListe = daten3D.readlines()
	laenge = len(daten3DListe)
	#laenge = len(re_n.split(daten3DListe))
	testCoord = re_whitespace.split(daten3DListe[0])
	
	#print daten3DListe[0]
	#print laenge/3
	#print testCoord[0] 
	
except:
	print ''' Cannot read/print daten3D.txt '''
	

newCoordsList = []

for i in range(laenge):
	coord = re_whitespace.split(daten3DListe[i])
	print coord
	
	xCoord = float(coord[0])
	yCoord = float(coord[1])
	zCoord = float(coord[2])	
	
	newCoord = [xCoord,yCoord,zCoord]			
	print newCoord
	newCoordsList.append(newCoord)
	
	
print newCoordsList	


	#yCoord = float(coord[1])
	#zCoord = float(coord[2])
	#newCoord[]	
	#coord[i] = re_whitespace.split(daten3DListe[i])
	#print coord[i]
	

	
