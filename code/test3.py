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
name = 'maze6'

imgnb = scipy.ndimage.imread('../res/'+name+'.png',mode='L')

#affichage de l'image originale
plt.figure()
plt.imshow(imgnb,interpolation='nearest',cmap='gray') 

#calcul de la metrique
W = 1./(0.001+imgnb)

#%% calcul de la map distance T

p0 = (19,399)
m = classMap.DistanceMap(p0,W)
m.calculerDistance()
T = m.distanceMap()
np.save('../result/'+name+'.npy',T)

#%% affichage de T

plt.plasma()
plt.figure()
plt.imshow(T,interpolation='nearest')
plt.scatter(p0[1],p0[0],c='r')
plt.title("solution de l'équation d'Eikonal |grad(T)|=F")


#%% calcul de la géodesic

I,J = m.calculGeodesic((398,331),alpha=0.05,it_max=300000)

#%% affichage de la géodesique
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(T,interpolation='nearest',cmap='plasma')
ax.imshow(imgnb,interpolation='nearest',cmap='gray')
ax.plot(J,I,c='g',linewidth=2)
#ax.set_ylim((T.shape[0],0))
#ax.set_xlim((0,T.shape[1]))
#ax.scatter(J,I,c='w',s=2)
ax.set_title("géodesique")
plt.show()

#%%sauvegarde de T

np.save('../result/'+name+'.npy',T)
