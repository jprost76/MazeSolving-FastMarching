# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 18:02:38 2019

@author: jprost

faire tourner dans une console python (et non ipython) 
pour visualiser l'animation

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import classMap
import scipy.ndimage

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

#choix de l'image
F=F1
Ft = 256 - F
plt.figure()
plt.gray()
plt.imshow(F,interpolation='nearest') 

#%%
F2 = imgnb = scipy.ndimage.imread("../res/maze.png",mode='L')
Ft2 = 256 - F2
plt.figure()
plt.gray()
plt.imshow(F2,interpolation='nearest')
#%% affichage rapide

p0 = np.array((315,169))
m = classMap.DistanceMap(p0,Ft2)

fig,ax = plt.subplots()

plt.plasma()
im = plt.imshow(m.distanceMap())
#im = plt.imshow(Ft,interpolation='nearest', animated=True,cmap='Greys')


def updatefig(*args):
    m.iterate()
    T = m.distanceMap()
    im.set_array(T)
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=1, blit=False,repeat='False')
plt.show()

#%% affichage avec superposition sur l'image initiale (trop lent!)

p0 = np.array((4,3))
m = classMap.DistanceMap([p0],Ft)

fig,ax = plt.subplots()

#im = plt.imshow(m.distanceMap())
im = plt.imshow(Ft,interpolation='nearest', animated=True,cmap='Greys')

def updatefig(*args):
    m.iterate()
    T = m.distanceMap()
    T_masked = np.ma.masked_array(T,np.isinf(T))
    ax.imshow(T_masked,cmap='plasma')

ani = animation.FuncAnimation(fig, updatefig, interval=5, blit=False,repeat='False')
plt.show()

