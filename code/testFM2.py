# -*- coding: utf-8 -*-
"""
Created on Wed May  1 18:17:59 2019

@author: jprost
"""

import matplotlib.pyplot as plt
import numpy as np
from classMap import DistanceMap
import scipy.ndimage

#%% chargement de l'image
name = 'maze3'

img = plt.imread('../res/'+name+'.png')[:,:,0]
plt.imshow(img,interpolation='nearest',cmap='gray') 
#%noir = 0, blanc=1
imgnb = np.zeros(img.shape)
imgnb[np.where(img!=0)] = 1
 #%%
plt.imshow(imgnb,interpolation='nearest',cmap='gray')

#%% calcul de la vitesse (premier FastMarching)

sinit = np.where(imgnb==0)
linit = list(zip(sinit[0],sinit[1]))

m1 = DistanceMap(linit,imgnb)
m1.calculerDistance()

T1 = m1.distanceMap()
plt.hot()
plt.figure()
plt.imshow(T1,interpolation='nearest')


#%% second fast Marching
#vitesse : proportionnelle à la distance au bord
Vit = T1/np.max(T1)
W = 1./(0.0001+imgnb) + 10./(0.0001+Vit)

p0 = (45,3)
m2  = DistanceMap([p0],W)
m2.calculerDistance()
T2 = m2.distanceMap()
#%
plt.hot()
plt.figure()
plt.imshow(T2,interpolation='nearest')
plt.scatter([p0[1]],[p0[0]],c="Green",s=30)

#%
I,J = m2.calculGeodesic((4,150),alpha=0.05,it_max=300000)

#%% affichage de la géodesique
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.imshow(T2,interpolation='nearest',cmap='plasma')
ax.imshow(imgnb,interpolation='nearest',cmap='gray')
ax.plot(J,I,c='g',linewidth=2.5)
ax.set_ylim((imgnb.shape[0],0))
ax.set_xlim((0,imgnb.shape[1]))
plt.show()


