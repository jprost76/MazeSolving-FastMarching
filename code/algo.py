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
    heappush(Q,(T[i,j],u))
        
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
        u = heappop(Q)
        print("it = ",it,", |Q| = ",len(Q),", u = ",u)
        iu = u[1][0]
        ju = u[1][1]
        A.append(u[1])
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
        
# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy as np
import math

class Sommet:
    def __init__(self,stat,val):
        self.statut = stat
        self.value = val
        
    def setStatutFront(self):
        self.statut = "FRONT"
        
    def setStatutFar(self):
        self.statut = "FAR"
    
    def setStatutVisited(self):
        self.statut = "VISITED"
    
    def getValue(self):
        return self.value
        
    def isFar(self):
        return (self.statut == "FAR")
        
    def isFront(self):
        return (self.statut == "FRONT")
        
    def isVisited(self):
        return (self.statut == "VISITED")
        
    def setValue(self,val):
        self.value = val

class DistanceMap():
    def __init__(self,SInit,Haut,Larg):
        self.hauteur = Haut
        self.largeur = Larg
        self.Map = [[Sommet("FAR",math.inf) for j in range(Larg)] for i in range(Haut)]
        for s in SInit(): #s = (i,j)
            i = s[0]
            j = s[1]
            if ((i<Haut) & (j<Larg)):
                self.Map[i][j].setValue(0)
                self.Map[i][j].setStatutVisited()
                for v in self.VoisinsNonVisites(i,j):
                    self.Map[i][j].setStatutFront()
                    
    def CoordValides(self,i,j):
        return ((i>=0) & (i<self.hauteur) & (j>=0) & (j<self.largeur))
        
    def VoisinsNonVisites(self,i,j):
        res = [] 
        if (self.CoordValides(i+1,j) & (not self.Map[i+1][j].isVisited())):
            res.append((i+1,j))
        if ((self.CoordValides(i-1,j)) & (not self.Map[i-1][j].isVisited())):
            res.append((i-1,j))       
        if (self.CoordValides(i,j-1) & (not self.Map[i][j-1].isVisited())):
            res.append((i,j-1))
        if (self.CoordValides(i,j+1) & (not self.Map[i][j+1].isVisited())):
            res.append((i,j+1))
        return res
        
    def afficheStatut(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if (self.Map[i][j].isVisited()):
                    print('*',end='')
                if (self.Map[i][j].isFront()):
                    print('-',end='')
                if (self.Map[i][j].isFar()):
                    print('.',end='')
            print()

     