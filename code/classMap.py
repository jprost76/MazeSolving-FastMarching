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
from numpy.linalg import norm
from scipy import interpolate
from scipy import optimize
import heapq

class Sommet:
    """
        un sommet de la grille
        
        attributs:
        -statut :"FRONT", "FAR", "VISITED"
        -value : valeur de la fonction T sur le sommet
    """
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
    """
        classe permettant de résoudre l'équation d'Eikonal |gradT| = F,
        avec la méthode de fast marching
    """
    def __init__(self,sinit,f):
        """
            initialise l'objet distance Map
            
            :param sinit: liste des sommet initiaux (tq T(x,y)=0) sinit = [(i0,j0),(i1,j1),...]
            :param f: numpy.ndarray 2D correspondant au second membre de l'équation d'Eikonal (image)
            
        """
        self.p0 = sinit[0]
        self.hauteur = f.shape[0]
        self.largeur = f.shape[1]
        self.Map = [[Sommet("FAR",math.inf) for j in range(f.shape[1])] for i in range(f.shape[0])]
        self.listeFront = []
        self.F = f
       
        for (i,j) in sinit:
            if ((i<f.shape[0]) & (j<f.shape[1])):
                self.Map[i][j].setValue(0)
                self.Map[i][j].setStatutVisited()
                for v in self.VoisinsNonVisites(i,j):
                    self.update(v)
     
    def loadMap(self,T):
        """
            Permet de charger une fonction T déja calcalulé.
            attribue a chaque sommet (i,j) la valeur  T[i,j].
            
            :param T : ndarray de meme dimension que F
        """                                           
        if (self.F.shape != T.shape):
            print("erreur : dimensions invalides.\n T doit etre de dimension ",self.F.shape)
        else : 
            for i in range(self.hauteur):
                for j in range(self.largeur):
                    self.Map[i][j].setValue(T[i,j])
                    self.Map[i][j].setStatutVisited()
        
    def CoordValides(self,i,j):
        """
            retourne un booleén, true si les coordonnées (i,j) sont valides,
            ie rentrent dans les dimensions de l'image F
        """
        return ((i>=0) & (i<self.hauteur) & (j>=0) & (j<self.largeur))
        
    def VoisinsNonVisites(self,i,j):
        """
            retourne la liste des sommets voisins non visités d'un sommet de coordonnées (i,j)
        """
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
        """
            (re)calcul la valeur de T au sommet v=(i_v,j_v)
        """
        i = v[0]
        j = v[1]
# on traite les cas ou le sommet v est situé sur un bord
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
#l'ancienne valeur du sommet
        Told = self.Map[i][j].getValue()
  
        if ( t < Told ):
#actualisation de la valeur T(i,j)            
            self.Map[i][j].setValue(t)
#actualisation de la listeFront
            if (self.Map[i][j].isFar()):
                heapq.heappush(self.listeFront,(t,v))
                self.Map[i][j].setStatutFront()
            else :
#si le sommet est deja sur le front
                index_sommet = self.listeFront.index((Told,v))
                self.listeFront[index_sommet] = (t,v)
                heapq.heapify(self.listeFront)
                
            
     
     
    def iterate(self):
        """ 
            réalise une itération de l'algo du fast marching
        """
        # recherche du minium parmis les sommets du front
        #TODO : optimiser la recherche du minimum avec un tri par tas (import heapq?)
        
        u = heapq.heappop(self.listeFront)
        
        iu = u[1][0]
        ju = u[1][1]   
        self.Map[iu][ju].setStatutVisited()
        for v in self.VoisinsNonVisites(iu,ju):
            self.update(v)
    
    def calculerDistance(self):
        """
            resoud l'équation d'Eikonal avec la méthode du fast marching
        """
        while (self.listeFront != []) :
            self.iterate()
        
    def afficheStatut(self):
        """
            fonction qui affiche le statut des sommets (utile pour le débuggage)
        """
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
        """
            affiche la valeur de T en chaque sommet (utile pour le débuggage)
        """
        for i in range(self.hauteur):
            for j in range(self.largeur):
                print("%5.2f"%self.Map[i][j].getValue(),end='')
            print()
        print('\n')
    
    def distanceMap(self):
        """ 
            retourne la solution de l'équation d'Eikonal T
            la fonction calculerDistance() doit être appelée avant    
        """
        D = np.zeros(self.F.shape)
        for i in range(self.hauteur):
            for j in range(self.largeur):
                D[i,j] = self.Map[i][j].getValue()
        return D
    
    

    def calculGeodesic(self,pi,alpha=0.1,it_max=100000):
        """
            calcul le plus court chemin du point p au point p0 (le point initial) 
            en utilisant la descente du gradient sur T. 
            la fonction calculerDistance() doit être appelée avant.
            
            :param pi : point de départ de la descente du gradient p=(i,j)
            :param alpha : pas de la descente du gradient
            :param it : nombre d'itérations max
            
            :return I : liste des coordonnées en i des points obtenues aux iterations de la descente
            :return J : liste des coordonnées en J des points obtenues aux iterations de la descente
            ex : ax.scatter(J,I)
        """
        
        gradT = np.gradient(self.distanceMap())
        p = np.array(pi)
        p0 = np.array(self.p0)
        it = 0
        I = []
        J = []
        while ((norm(p-p0,2)>1) and (it<it_max)):
            I.append(p[0])
            J.append(p[1])
#sommet le plus proche de p dans la grille
            ip = int(round(p[0]))
            jp = int(round(p[1]))
            if (ip >= self.hauteur):
                ip = self.hauteur - 1
            if (ip < 0):
                ip = 0
            if (jp >= self.largeur):
                jp = self.largeur - 1
            if (jp < 0):
                jp = 0
            
            gradTp = np.array(( gradT[0][ip,jp] , gradT[1][ip,jp]))
            p = p - alpha*gradTp/norm(gradTp,2)
            it += 1
            
        return I,J
      
    def calculGeodesicInter(self,pi,alpha=0.1,it_max=100000):
        #interpolation de T
        T_inter = interpolate.interp2d(np.arange(self.largeur),np.arange(self.hauteur),self.distanceMap(),kind='linear')
        
        def T_inter2(u):
            return T_inter(u[0],u[1])
            
        p = np.array(pi)
        
        sol = optimize.fmin_cg(T_inter2,p,maxiter=it_max,full_output=True,retall=True)
            
       # I = [p[1] for p in sol[-1]]
        #J = [p[0] for p in sol[-1]]
        return sol
