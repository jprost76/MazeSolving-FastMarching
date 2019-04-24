# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:04:33 2019

@author: jprost
"""

import matplotlib.pyplot as plt
import numpy as np
import classMap
import scipy.ndimage

#%% chargement de l'image

#imgnb = scipy.ndimage.imread("../res/lab_big_700.png",mode='L')
imgnb = scipy.ndimage.imread("../res/lab_big_700.png",mode='L')
plt.figure()
plt.imshow(imgnb,interpolation='nearest',cmap='gray') 

#metrique
W = 1./(0.001+imgnb)

#%% calcul de la map distance T

p0 = (561,547)
m = classMap.DistanceMap(p0,W)
m.calculerDistance()

#%% affichage de T
T = m.distanceMap()
plt.plasma()
plt.figure()
plt.imshow(T,interpolation='nearest')
plt.scatter(p0[1],p0[0],c='r')
plt.title("solution de l'équation d'Eikonal |grad(T)|=F")


#%% calcul de la géodesic

I,J = m.calculGeodesic((2,2),alpha=0.1,it_max=300000)

#%% affichage de la géodesique
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.imshow(T,interpolation='nearest',cmap='plasma')
ax.imshow(imgnb,interpolation='nearest',cmap='gray')
ax.plot(J,I,c='g',linewidth=2)
#ax.scatter(J,I,c='w',s=2)
ax.set_title("géodesique")
plt.show()

#%%sauvegarde de T

np.save('../result/maze2.npy',T)
