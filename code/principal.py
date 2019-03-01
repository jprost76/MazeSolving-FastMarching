
# -*- coding: utf-8 -*-
"""

"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.ndimage
from classMap import DistanceMap

img = mpimg.imread("labyrinth.png")
if img.dtype == np.float32: # Si le résultat n'est pas un tableau d'entiers
    img = (img * 255).astype(np.uint8)
    
#affiche l'image 
plt.imshow(img)
plt.show()
    
img.shape # les dimentions de l'image et le plan (lignes/colonnes/plan)
#ensuite on fait img[100, 120] pour avoir la valeur du pixel voulu.

# pour modifier un pixel : img[100, 120] = (56, 120, 355)

imgnb = scipy.ndimage.imread("labyrinth.png",mode='L')

m = DistanceMap([(100,100)],imgnb)

it=0;
while (m.listeFront != []):
#    r = 'x'
#    while (r!='o'):
#       r = input("continuer?(o/n)")
    it += 1;
    m.iterate()
    print("iteration ",it)
#    m.afficheStatut()
D = m.distanceMap()

plt.figure()
plt.imshow(D,interpolation='nearest')
plt.figure()
plt.imshow(imgnb,interpolation='nearest')


