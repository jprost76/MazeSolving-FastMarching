# -*- coding: utf-8 -*-
"""
Created on Wed May  1 18:17:59 2019

@author: jprost
"""

import matplotlib.pyplot as plt
import numpy as np
import classMap
import scipy.ndimage

#%% chargement de l'image
name = 'maze5'

img = scipy.ndimage.imread('../res/'+name+'.png',mode='L')
plt.imshow(img,interpolation='nearest',cmap='gray') 
#%noir = 0, blanc=1
imgnb = np.ones(img.shape)
imgnb[np.where(img==0)] = 0


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
W = 1./(0.01+imgnb) + 8./(0.001+Vit)

m2  = DistanceMap([(60,639)],W)
m2.calculerDistance()
T2 = m2.distanceMap()
plt.hot()
plt.figure()
plt.imshow(T2,interpolation='nearest')

#%
I,J = m2.calculGeodesic((253,1),alpha=0.05,it_max=300000)

#%% affichage de la géodesique
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.imshow(T2,interpolation='nearest',cmap='plasma')
ax.imshow(imgnb,interpolation='nearest',cmap='gray')
ax.plot(J,I,c='g',linewidth=2)
ax.set_ylim((imgnb.shape[0],0))
ax.set_xlim((0,imgnb.shape[1]))
plt.show()


#%%

#np.save('../result/'+name+'.npy',T)
