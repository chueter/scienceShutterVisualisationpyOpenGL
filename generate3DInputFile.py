#### should generate a file with 3 columns containig x y z position of atoms
###  to read them in with another module and 3d visualize them

import math

try:
    datenFile = file('daten3D.txt ','w')

except:
    print 'kann Datei daten3D.txt nicht erzeugen'

xKoordinaten = [1, 9]
yKoordinaten = [1, 9]
zKoordinaten = [1, 9]

#coord = [(0,0,0), (1,0,0)]
coord = [(i,j,k) for i in range(9) for j in range(9) for k in range(9)]


for i in coord:
	datenFile.write(str(i[0])+' '+str(i[1])+' '+str(i[2])+'\n')

datenFile.close()




