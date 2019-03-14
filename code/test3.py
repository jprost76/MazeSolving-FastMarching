# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 15:04:33 2019

@author: jprost
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy.linalg import norm
from classMap import DistanceMap
import scipy.ndimage

#%% chargement de l'image

imgnb = scipy.ndimage.imread("labyrinth.png",mode='L')
plt.figure()
plt.imshow(imgnb,interpolation='nearest') 

#inversion de l'image : noir "=" 255 , blanc "=" 1
F = 256 - imgnb

#%% calcul de la map distance T

p0 = np.array((290,300))
m = DistanceMap([p0],F)
m.calculerDistance()

#%% affichage de T
T = m.distanceMap()
plt.plasma()
plt.figure()
plt.imshow(T,interpolation='nearest')

#%% calcul de la geodesic en utilisant la descente du gradient
     
gradT = np.gradient(T)

# pas de la méthode du gradient
h = 0.1

#%%
gradT = np.gradient(T)

# pas de la méthode du gradient
h = 0.1

#point de départ
p = np.array((45,45))
#courbe
mu = []
it = 0;
while ((norm(p-p0,2)>1) and (it<1500)):
    mu.append(p)
    gradTp = np.array(( gradT[0][int(round(p[0])),int(round(p[1]))] , gradT[1][int(round(p[0])),int(round(p[1]))]))
    p = p - h*gradTp/norm(gradTp,2)
    print(norm(p-p0,2))
    it += 1
    
#%%

x = [p[1] for p in mu]
y = [p[0] for p in mu]
fig = plt.figure()
plt.hold('true')
ax = fig.add_subplot(111)
ax.imshow(T,interpolation='nearest')  
ax.scatter(x,y,c='r')
plt.show()