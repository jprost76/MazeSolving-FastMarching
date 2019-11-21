#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:20:15 2019

@author: jprost
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from classMap import DistanceMap

#image blanc=1, noir=0
F = 255*np.ones((50,50))
noir = 0
F[10,10:40] = noir
F[10:35,10] = noir

#metrique
W = 1./(0.001+F)

#affichage de l'image
plt.figure()
plt.gray()
plt.imshow(F,interpolation='nearest') 

#fast marching

s0 = [(14,14)]
m = DistanceMap(s0,W)

#%%
fig,ax = plt.subplots()
plt.imshow(W,interpolation='nearest', cmap='Greys')
#%%
it = 0
while (it<1768):
    m.iterate()
    it += 1

#%%
while (not m.algoFini()) :
    m.iterate()
    T = m.distanceMap()
    T_masked = np.ma.masked_array(T,np.isinf(T))
    if (it%5 == 0):
        ax.imshow(T_masked,cmap='plasma')
        plt.savefig('../result/animation2/frame'+str(it))
    it += 1
    
    