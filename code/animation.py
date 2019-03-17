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
p0 = np.array((4,3))
m = classMap.DistanceMap([p0],Ft)

#%%

fig = plt.figure()

plt.plasma()
im = plt.imshow(m.distanceMap(), animated=True)
#im = plt.imshow(F,interpolation='nearest')

def updatefig(*args):
    m.iterate()
    T = m.distanceMap()
    ret = T
    ret[np.isinf(T)] = Ft[np.isinf(T)]
    im.set_array(ret)
    return im,

ani = animation.FuncAnimation(fig, updatefig, interval=10, blit=False)
plt.show()