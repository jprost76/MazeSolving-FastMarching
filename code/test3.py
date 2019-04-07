# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:04:33 2019

@author: jprost
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy.linalg import norm
import classMap
import scipy.ndimage

#%% chargement de l'image

imgnb = scipy.ndimage.imread("../res/lab_big_500.png",mode='L')
plt.figure()
plt.imshow(imgnb,interpolation='nearest',cmap='gray') 

#inversion de l'image : noir "=" 255 , blanc "=" 1
F = 256 - imgnb

#%% calcul de la map distance T

p0 = (401,390)
m = classMap.DistanceMap(p0,F)
m.calculerDistance()

#%% affichage de T
T = m.distanceMap()
plt.plasma()
plt.figure()
plt.imshow(T,interpolation='nearest')
plt.scatter(p0[1],p0[0],c='r')

#%% calcul de la géodesic

I,J = m.calculGeodesic((1,1),alpha=0.05,it_max=300000)

fig = plt.figure()
plt.hold('true')
ax = fig.add_subplot(111)
ax.imshow(T,interpolation='nearest')  
ax.scatter(J,I,c='r')
plt.show()

#%%sauvegarde de T

np.save('../result/lab_big_500.npy',T)
