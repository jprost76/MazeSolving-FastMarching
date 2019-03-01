# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 18:24:39 2019

@author: jprost
"""

import numpy as np
from math import sqrt
from heapq import *
from enum import Enum
import matplotlib.pyplot as plt
    
def Update(u,Q,T,F) :
    """
        calcul la nouvelle valeur T du sommet u et actualise la liste 
        des sommets adjacents Q
    """ 
    i = u[0]
    j = u[1]
    T1 = min(T[i-1,j],T[i+1,j])
    T2 = min(T[i,j-1],T[i,j+1])
    if (abs(T1-T2)<F[i,j]):
        t = (T1+T2+sqrt(2*F[i,j]**2-(T1-T2)**2))*0.5
    else:
        t = min(T1,T2)+F[i,j]
    Told = T[i,j]
    T[i,j] = min(T[i,j],t)
    if ((Told,u) in Q):
        Q.remove((Told,u))
    Q.append((T[i,j],u))
        
def voisins(i,j,D,A):
    res = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    for S in res:
        i0 = S[0]
        j0 = S[1]
        if ((i0<0) or (i0>D[0]-1) or (j0<0) or (j0>D[1]-1) or ((i0,j0) in A)):
            res.remove((i0,j0))
    return res
    
def FastMarching(F,I):
    """ résoud l'équation d'Eikonal |grad(T)|=f, avec T inconnue
    
    Arguments :
    F -- numpy array 2D tel que : F[i,j] = f(i*deltax,j*delta_y)
    I -- liste des sommets connus initialement (T,(i,j))
    """
    #initialisation de T et Q
    Q = [] #sommets sur le front
    T = np.inf*np.ones(F.shape)
    A = [] #sommets accéptés
    for S in I : #S=(T,(i,j))
        A.append(S[1])
        t = S[0]
        i = S[1][0]
        j = S[1][1]
        T[i,j] = t
        for u in voisins(i,j,F.shape,A):
            Update(u,Q,T,F)
    it = 0
    print("fin initialisation")
    while (Q!=[]):
        it += 1
        u = min(Q)
        Q.remove(u)
        A.append(u[1])
        print("it = ",it,", |Q| = ",len(Q),", u = ",u)
        iu = u[1][0]
        ju = u[1][1]
        
        for v in voisins(iu,ju,F.shape,A):
            Update(v,Q,T,F)
        print("Q : ",Q)
        print("A : ",A)
        r='x'
        while(r!='o'):
            r = input("continuer? o/n")
            if (r == 'q'):
                quit()
    return T
        
        