# -*- coding: utf-8 -*-
"""

"""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
img = mpimg.imread("monimage.png")
if img.dtype == np.float32: # Si le résultat n'est pas un tableau d'entiers
    img = (img * 255).astype(np.uint8)
    
#affiche l'image 
plt.imshow(img)
plt.show()
    
img.shape # les dimentions de l'image et le plan (lignes/colonnes/plan)
#ensuite on fait img[100, 120] pour avoir la valeur du pixel voulu.

# pour modifier un pixel : img[100, 120] = (56, 120, 355)




