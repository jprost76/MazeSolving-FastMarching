# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:50:17 2019

@author: jprost
"""

# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import numpy as np
import math
import heapq

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

class DistanceMap:
    def __init__(self,SInit,f):
        self.hauteur = f.shape[0]
        self.largeur = f.shape[1]
        self.Map = [[Sommet("FAR",math.inf) for j in range(f.shape[1])] for i in range(f.shape[0])]
        self.listeFront = []
        self.F = f
        for s in SInit: 
            i = s[0]
            j = s[1]
            if ((i<f.shape[0]) & (j<f.shape[1])):
                self.Map[i][j].setValue(0)
                self.Map[i][j].setStatutVisited()
                for v in self.VoisinsNonVisites(i,j):
                    self.update(v)
                                                   
    def CoordValides(self,i,j):
        return ((i>=0) & (i<self.hauteur) & (j>=0) & (j<self.largeur))
        
    def VoisinsNonVisites(self,i,j):
        res = [] 
        if (self.CoordValides(i+1,j)):
            if (not self.Map[i+1][j].isVisited()):
                res.append((i+1,j))
        if (self.CoordValides(i-1,j)):
            if (not self.Map[i-1][j].isVisited()):
                res.append((i-1,j))       
        if (self.CoordValides(i,j-1)):
            if (not self.Map[i][j-1].isVisited()):
                res.append((i,j-1))
        if (self.CoordValides(i,j+1)):
            if (not self.Map[i][j+1].isVisited()):
                res.append((i,j+1))
        return res
    
    
    def update(self,v):
        i = v[0]
        j = v[1]
        if (i==0):
            T1 = self.Map[i+1][j].getValue()
        else : 
            if (i==self.hauteur-1) :
                T1 = self.Map[i-1][j].getValue()
            else :
                T1 = min(self.Map[i+1][j].getValue(),self.Map[i-1][j].getValue())
        if (j==0):
            T2 = self.Map[i][j+1].getValue()
        else : 
            if (j==self.largeur-1) :
                T2 = self.Map[i][j-1].getValue()
            else :
                T2 = min(self.Map[i][j+1].getValue(),self.Map[i][j-1].getValue())
        if (abs(T1-T2) < self.F[i,j]):
            t = (T1+T2+math.sqrt(2*self.F[i,j]**2-(T1-T2)**2))*0.5
        else:
            t = min(T1,T2)+self.F[i,j]
        Told = self.Map[i][j].getValue()
        if ( t < Told ):
            self.Map[i][j].setValue(t)
            if ((Told,v) in self.listeFront):
                self.listeFront.remove((Told,v))
                heapq.heappush(self.listeFront,(t,v))
        else :
            if (not ((Told,v) in self.listeFront)):
                heapq.heappush(self.listeFront,(Told,v))
     
    def iterate(self):
        u = heapq.heappop(self.listeFront)
        iu = u[1][0]
        ju = u[1][1]   
        self.Map[iu][ju].setStatutVisited()
        for v in self.VoisinsNonVisites(iu,ju):
            self.update(v)
    
    def calculerDistance(self):
        while (self.listeFront != []) :
            self.iterate()
        
    def afficheStatut(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if (self.Map[i][j].isVisited()):
                    print('*',end=' ')
                if (self.Map[i][j].isFront()):
                    print('-',end=' ')
                if (self.Map[i][j].isFar()):
                    print('.',end=' ')
            print()
        print('\n')

    def afficheDistance(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                print("%5.2f"%self.Map[i][j].getValue(),end='')
            print()
        print('\n')
    
    def distanceMap(self):
        D = np.zeros(self.F.shape)
        for i in range(self.hauteur):
            for j in range(self.largeur):
                D[i,j] = self.Map[i][j].getValue()
        return D

