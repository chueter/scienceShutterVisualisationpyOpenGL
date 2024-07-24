#! /usr/bin/python
from sys import argv, exit
import datetime
from re import *

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Fehler: PyOpenGL not installed properly !!'''
  sys.exit(  )

from stereoCamera import StereoCamera
sC = StereoCamera( )

ESCAPE = '\033'

animationAngle = 0.0
frameRate = 120
stereoMode = "NONE"
lightColors = {
	"white":(1.0, 1.0, 1.0, 1.0),
	"red":(1.0, 0.0, 0.0, 1.0),
	"green":(0.0, 1.0, 0.0, 1.0),
	"blue":(0.0, 0.0, 1.0, 1.0)
}

lightPosition = (5.0, 5.0, 20.0, 1.0)

from time import sleep
		
def animationStep( ):
	"""Update animated parameters."""
	global animationAngle
	global frameRate
	animationAngle += 0 # 2
	while animationAngle > 360:
		animationAngle -= 360
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

def setLightColor( s ):
	"""Set light color to 'white', 'red', 'green' or 'blue'."""
	if lightColors.has_key( s ):
		c = lightColors[ s ]
		glLightfv( GL_LIGHT0, GL_AMBIENT, c )
		glLightfv( GL_LIGHT0, GL_DIFFUSE, c )
		glLightfv( GL_LIGHT0, GL_SPECULAR, c )

def render( side ):
	"""Render scene in either GLU_BACK_LEFT or GLU_BACK_RIGHT buffer"""
	glViewport( 0, 0,
		glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT ))
	if side == GL_BACK_LEFT:
		f = sC.frustumLeft
		l = sC.lookAtLeft
	else:
		f = sC.frustumRight
		l = sC.lookAtRight
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glFrustum( f[0], f[1], f[2], f[3], f[4], f[5] )
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt( l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8] )
	
	glRotatef( angleX, 1.0, 0.0, 0.0 )	
	glRotatef( angleZ, 0.0, 0.0, 1.0 )
	
	glTranslate(xcam, ycam, zcam)
	
	# stationary objects
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1] )
	glCallList( teapotList )
	
	# objects that change in time
	now         = datetime.datetime.now()
	micro       = now.microsecond
	hour        = now.hour
	minute      = now.minute
	second      = now.second
	
	glRotate(-(second+micro/1000000.0)*60*3, 0.0, 1.0, 1.0)
	glTranslate(1.5, 0.0, 0.0)
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.2, 1.0] )
	glRotate((second+micro/1000000.0)*60*5, 0.0, 1.0, 1.0)
	glutSolidTeapot(0.3)
	glRotate(-(second+micro/1000000.0)*60*5, 0.0, 1.0, 1.0)

	
	glRotate((second+micro/1000000.0)*60*2, 0.0, 1.0, 1.0)
	glTranslate(-1.5, 1.0, 0.0)
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.8, 0.2, 0.2, 1] )
	glutSolidSphere(0.2,16,16)

def display(  ):
	"""Glut display function."""
    
	if stereoMode != "SHUTTER":
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	if stereoMode == "SHUTTER":
		setLightColor( "white" )
		glDrawBuffer( GL_BACK_LEFT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		render( GL_BACK_LEFT )
		glDrawBuffer( GL_BACK_RIGHT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		render( GL_BACK_RIGHT )
	elif stereoMode == "ANAGLYPH":
		glDrawBuffer( GL_BACK_LEFT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		setLightColor( "red" )
		render( GL_BACK_LEFT )
		glClear( GL_DEPTH_BUFFER_BIT )
		glColorMask( False, True, False, False )
		setLightColor( "green" )
		render( GL_BACK_RIGHT )
		glColorMask( True, True, True, True )
	else:
		glDrawBuffer(GL_BACK_LEFT)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		setLightColor( "white" )
		render(GL_BACK_LEFT)
	glutSwapBuffers( )

def UpdateCamera():
	global sC
	global basis
	sC.aperture = 40.0
	sC.focalLength = 10.0
	sC.centerPosition[0], sC.centerPosition[1], sC.centerPosition[2] = \
		0.0, 0.0, 5.0
	sC.viewingDirection[0], sC.viewingDirection[1], sC.viewingDirection[2] = \
		0.0, 0.0, -1.0
	sC.near = sC.focalLength / 500.0
	sC.far = 1000
	sC.eyeSeparation = sC.focalLength / basis
	sC.whRatio = float( glutGet( GLUT_WINDOW_WIDTH ) ) /  glutGet( GLUT_WINDOW_HEIGHT )
	sC.update( )


def init(  ):
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


	"""Glut init function."""
	glClearColor ( 0, 0, 0, 0 )
	glEnable( GL_DEPTH_TEST )
	glShadeModel( GL_SMOOTH )
	glEnable( GL_LIGHTING )
	glEnable( GL_LIGHT0 )
	glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, 0 )
	glLightfv( GL_LIGHT0, GL_POSITION, [4, 4, 4, 1] )
	lA = 0.8
	glLightfv( GL_LIGHT0, GL_AMBIENT, [lA, lA, lA, 1] )
	lD = 1
	glLightfv( GL_LIGHT0, GL_DIFFUSE, [lD, lD, lD, 1] )
	lS = 1
	glLightfv( GL_LIGHT0, GL_SPECULAR, [lS, lS, lS, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.7, 0.7, 0.7, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1] )
	glMaterialf( GL_FRONT_AND_BACK, GL_SHININESS, 50 )
	
	# these are the static objects, which do not change
	global teapotList
	teapotList = glGenLists( 1 )
	glNewList( teapotList, GL_COMPILE )
	# glutSolidTeapot( 0.5 )
	#glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.8, 0.2, 0.2, 1] )
	#glutSolidSphere(0.2,16,16)
	for i in newCoordsList:
		glTranslate(i[0], i[1], i[2])
		#glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.8, 0.2, 0.2, 1] )
		glutSolidSphere(0.2,16,16)
		glTranslate(-i[0], -i[1], -i[2])
	glEndList( )
	
	UpdateCamera()
	
def reshape( width, height ):
	"""Glut reshape function."""
	sC.whRatio = float(width)/float(height)
	sC.update( )

def keyPressed(*args):
	global xcam
	global ycam
	global zcam
	global angleX
	global angleZ
	global basis
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		sys.exit()
	elif args[0] == 'r':
		xcam = 0.0
		ycam = 0.0
		zcam = 0.0
		angleX = 0.0
		angleZ = 0.0
	elif args[0] == 'j':
		angleZ += 1.0
	elif args[0] == 'l':
		angleZ -= 1.0
	elif args[0] == 'i':
		angleX += 1.0
	elif args[0] == 'm':
		angleX -= 1.0
	elif args[0] == 'k':
		angleX = 0.0
		angleZ = 0.0
	elif args[0] == 'b':
		basis *= 1.05
		UpdateCamera()
	elif args[0] == 'B':
		basis /= 1.05
		UpdateCamera()


def MouseWithoutKey(*args):
	global xcam
	global ycam
	global zcam
	# print "Mouse is moving", args[0], args[1]
	width = float( glutGet( GLUT_WINDOW_WIDTH ) )
	height = float( glutGet( GLUT_WINDOW_HEIGHT ) )
	xcam = (2.0*float(args[0]) - width) / (0.5*width)
	ycam = (height - 2.0*float(args[1])) /(0.5*height)

def specialKey(*args):
	global xcam
	global ycam
	global zcam
	# print "Special key pressed"
	if args[0] == GLUT_KEY_LEFT:
		xcam -= 0.05
	elif args[0] == GLUT_KEY_RIGHT:
		xcam += 0.05
	elif args[0] == GLUT_KEY_UP:
		ycam += 0.05
	elif args[0] == GLUT_KEY_DOWN:
		ycam -= 0.05
	elif args[0] == GLUT_KEY_PAGE_UP:
		zcam += 0.05
	elif args[0] == GLUT_KEY_PAGE_DOWN:
		zcam -= 0.05
		

######## main program ##########

teapotList = 0
xcam = 0.0
ycam = 0.0
zcam = 0.0
angleX = 0.0
angleZ = 0.0
basis = 200.0

if len( argv ) != 2:
	print "Usage:"
	print "python stereDemo.py SHUTTER | ANAGLYPH | NONE \n"
else:
	glutInit( sys.argv )
	stereoMode = sys.argv[1].upper( )
	if stereoMode == "SHUTTER":
		glutInitDisplayMode( GLUT_STEREO | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
	else:
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
            
	glutInitWindowSize( 500, 500 )
	glutInitWindowPosition( 100, 100 )
	glutCreateWindow( sys.argv[0] )
	init(  )
	
	glutFullScreen( )

	glutDisplayFunc( display )
	glutReshapeFunc( reshape )
	
	glutKeyboardFunc( keyPressed )
	
	glutSpecialFunc( specialKey)
	
	glutPassiveMotionFunc(MouseWithoutKey)
	
	glutIdleFunc( animationStep )
	glutMainLoop(  )
