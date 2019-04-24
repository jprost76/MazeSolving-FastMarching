# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 21:14:42 2019

@author: jprost

charge une distance map préalablement enregistré sous le format .npy


"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm
import classMap
import scipy.ndimage

#%% chargement de l'image

imgnb = scipy.ndimage.imread("../res/lab_big_700.png",mode='L')
plt.figure()
plt.imshow(imgnb,interpolation='nearest',cmap='gray') 

#inversion de l'image : noir "=" 255 , blanc "=" 1
F = 256 - imgnb

#%%

p0 = (560,549)
T = np.load('../result/lab_big_700.npy')
m = classMap.DistanceMap(p0,F)
m.loadMap(T)

#%%
I,J  = m.calculGeodesic((488,426),it_max=300000,alpha=1.0)

#%
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(T,cmap='plasma',interpolation='nearest')  
ax.scatter(J,I,c='g',s=2)
ax.set_xlim((0,T.shape[1]))
ax.set_ylim((T.shape[0],0))
plt.show()