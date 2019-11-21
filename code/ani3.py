# -*- coding: utf-8 -*-
"""
Created on Tue May 28 20:52:20 2019

@author: jprost
"""
from copy import copy

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as colors
import classMap
import scipy.ndimage

from matplotlib.animation import FFMpegWriter
writer = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)

#choix du labyrinthe
name = 'maze'

#chargement de l'image
img = plt.imread('../res/'+name+'.png')[:,:,0]
plt.imshow(img,interpolation='nearest',cmap='gray') 
#%noir = 0, blanc=1
imgnb = np.zeros(img.shape)
imgnb[np.where(img!=0)] = 1

#colormap speciale
palette = copy(plt.cm.hot)
palette.set_under('black', 1.0)
palette.set_over('black', 1.0)
palette.set_bad('white', 1)

#%% calcul de la vitesse

sinit = np.where(imgnb==0)
linit = list(zip(sinit[0],sinit[1]))
W1 = 1./(0.001+imgnb)
m1 = classMap.DistanceMap(linit,W1)

#animation du calcul de la vitesse?
anim_vit = False

if (anim_vit == True):
   fig = plt.figure()
   ims1 = []
   im = plt.imshow(m1.distanceMap())
   i =0
   while (m1.algoFini() == False) :
      m1.iterate()
      i += 1
      if (i%100 == 0):
          T = m1.distanceMap()
          #les murs
          T[((T==np.inf)&(imgnb==0))] = -1
          T_max = np.max(T[(T!=np.inf) & (imgnb!=0)] )
          T_masked = np.ma.masked_array(T,np.isinf(T))
          im = plt.imshow(T_masked,cmap=palette,vmin=0,vmax=T_max,animated=True)
          ims1.append([im])
             
   ani1 = animation.ArtistAnimation(fig, ims1, interval=2, blit=True,repeat_delay=100)
   plt.show()
else:
    m1.calculerDistance()
    
T1 = m1.distanceMap()
   
    

#%% ff2



p0 = [(317,168)]
Vit = T1/np.max(T1)
W = 1./(0.0001+imgnb) + 10./(0.0001+Vit)
m = classMap.DistanceMap(p0,W)

#animation oui/non?
anim_ff = True

if (anim_ff==True):
    fig = plt.figure()
    ims = []
    im = plt.imshow(m.distanceMap())
    #%
    i = 0
    while (m.algoFini() == False) :
       m.iterate()
       i += 1
       if (i%100 == 0):
          T = m.distanceMap()
           #mur a -1
          T[((T==np.inf)&(imgnb==0))] = -1
          T_max = np.max(T[(T!=np.inf) & (imgnb!=0)] )
          T_masked = np.ma.masked_array(T,np.isinf(T))
          im = plt.imshow(T_masked,cmap=palette,vmin=0,vmax=T_max,animated=True)
          ims.append([im])
    #%
    ani = animation.ArtistAnimation(fig, ims, interval=5, blit=True,repeat_delay=500)

    plt.show()
else:
    m.calculerDistance()
    T2 = m.distanceMap()
    
#%% gradient a corriger!
    
    
I,J = m.calculGeodesic((4,175))
anim_grad = True

if (anim_grad==True):
    fig,ax = plt.subplots()
    Y = []
    X = []
    
    fig = plt.figure()
    ims = []
    im = plt.imshow(imgnb)
    #%
    for i in range(len(I)):
        if (i%10 == 0):
            ax.imshow(imgnb,interpolation='nearest',cmap='gray')
            ax.set_ylim((imgnb.shape[0],0))
            ax.set_xlim((0,imgnb.shape[1]))
            im = ax.plot(J[0:i],I[0:i],c='g',linewidth=2.5,animated=True)
            ims.append([im])
    
    
        
    anim3 = animation.FuncAnimation(fig,animate,frames=1000,init_func=init,interval=5,blit=True
    )
    plt.show()
    
    
