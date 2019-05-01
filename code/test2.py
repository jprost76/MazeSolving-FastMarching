# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 13:58:10 2019

@author: jprost
"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy.linalg import norm
from classMap import DistanceMap

#%% petites images de test

F1 = 255*np.ones((50,49))
noir = 1
F1[1,0:47] = noir
F1[5,0:15] = noir
F1[5:40,20] = noir
F1[5,20:43] = noir
F1[1:46,47] = noir
F1[40,20:44] = noir
F1[5:47,15] = noir
F1[46,15:48] = noir
F1[5:40,43] = noir

F2 = 255*np.ones((50,50))
noir = 1
F2[10,10:40] = noir
F2[10:35,10] = noir

#%%choix de l'image
F=F1
Ft = 256 - F
plt.figure()
plt.gray()
plt.imshow(F,interpolation='nearest') 

#%% calcul de la fonction distance T
p0 = [(25,30)]
m = DistanceMap(p0,Ft)
m.calculerDistance()


T = m.distanceMap()
plt.hot()
plt.figure()
plt.imshow(T,interpolation='nearest')
     
#%% calcul de la geodesic en utilisant la descente du gradient (à améliorer : interpolation du gradient)
     
I,J = m.calculGeodesic((43,44))
    
#%%

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(T,cmap='plasma',interpolation='nearest')  
ax.plot(J,I,c='r')
plt.show()

