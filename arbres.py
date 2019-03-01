# -*- coding: utf8 -*-
## abres.py 1.4
## Copyright Laurent Signac (28/03/2012)
##
## Laurent.Signac@univ-poitiers.fr
##
## Ce logiciel est un module Python
## permettant de manipuler des arbres
##
## Ce logiciel est régi par la licence CeCILL-C soumise au droit français et
## respectant les principes de diffusion des logiciels libres. Vous pouvez
## utiliser, modifier et/ou redistribuer ce programme sous les conditions
## de la licence CeCILL-C telle que diffusée par le CEA, le CNRS et l'INRIA
## sur le site "http://www.cecill.info".
##
## En contrepartie de l'accessibilité au code source et des droits de copie,
## de modification et de redistribution accordés par cette licence, il n'est
## offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
## seule une responsabilité restreinte pèse sur l'auteur du programme,  le
## titulaire des droits patrimoniaux et les concédants successifs.
##
## A cet égard  l'attention de l'utilisateur est attirée sur les risques
## associés au chargement,  à l'utilisation,  à la modification et/ou au
## développement et à la reproduction du logiciel par l'utilisateur étant
## donné sa spécificité de logiciel libre, qui peut le rendre complexe à
## manipuler et qui le réserve donc à des développeurs et des professionnels
## avertis possédant  des  connaissances  informatiques approfondies.  Les
## utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
## logiciel à leurs besoins dans des conditions permettant d'assurer la
## sécurité de leurs systèmes et ou de leurs données et, plus généralement,
## à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
##
## Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
## pris connaissance de la licence CeCILL-C, et que vous en avez accepté les
## termes.
## http://www.cecill.info/licences/Licence_CeCILL-C_V1-fr.txt
##

## Corrections :
## 13/04/2015 : ajout de label="" dans les attributs d'une arête
## Ajout des méthodes sageGraph et sageView pour interagir avec Sage
## corrections sur type, __class__ pour avoir la compatibilité python 2

import subprocess

__version__ = '1.4'

def Property(func) :
    return property(**func())

#def _isa(instance, classe ) :
#    if instance.__class__==classe : return True
#    for b in instance.__bases__ :
#        if _isa(b,classe) : return True
#    return False
class Arbre :
    """ Classe pour représenter des arbres """

    def __fromlist(self,liste) :
        """ Construit un arbre à partir de listes """
        assert(isinstance(liste, list) or isinstance(liste, tuple))
        assert(len(liste)>=1)
        self.__label=liste[0]
        for sa in liste[1:] :
            self._fils.append(Arbre(sa))

    def __init__(self, first, **kwargs) :#label, listefils=None) :
        """
        Crée un arbre à partir
        1) d'un label et d'une liste de sous arbres éventuels
        2) Si le premier argument est une liste ou un tuple, il doit
           "bien construit" : en premier élément un label et en second
           élément une liste de fils suivant le même schéma.
        3) Un autre arbre (copie en profondeur)
        Exemple :
        a=Arbre('A',fils=[Arbre('B',Arbre('C')])
        b=Arbre(( 'A',(('B',('C')),'D') ))

        L'étiquette d'un noeud ne DOIT PAS être None
        """
        assert(first!=None)
        self.__label=None
        self._fils=[]
        if isinstance(first,list) or isinstance(first,tuple) :
            self.__fromlist(first)
        elif isinstance(first,Arbre) :
            self.__label=first.racine
            for sa in first._fils :
                if sa==None : self._fils.append(None)
                else : self._fils.append(Arbre(sa))
        else :
            self.__label=first
            self._fils=kwargs.get('fils',[])


    def sageGraph(self):
        """ Renvoie une description (dictionnaire)
        permettant de créer un graphe dans Sage
        """
        res = dict()
        res[self.racine] = []
        for fils in self:
            desc = fils.sageGraph()
            res[self.racine].append(fils.racine)
            res.update(desc)
        return res


    def sageView(self):
        """ Visualise l'arbre dans sage """
        from sage.graphs.digraph import DiGraph
        g = DiGraph(self.sageGraph())
        p = g.plot(layout='tree')
        p.show()

    def __get_racine(self) :
        return self.__label
    def __set_racine(self, label) :
        self.__label=label
    racine=property(__get_racine,__set_racine,doc="Accède ou modifie le label de la racine")

    def ajoute(self,a) :
        """ Ajoute l'arbre a comme nouveau fils de la racine
        (en fin de liste)
        """
        assert(isinstance(a,Arbre))
        self._fils.append(a)

    def remplace(self,pos,a) :
        """ Remplace le fils de la racine situé en position pos par
        l'arbre a.
        """
        if pos<0 : pos=len(self._fils)-pos
        if pos<0 : raise IndexError('Position '+pos+' incorrecte')
        if pos>=len(self._fils) : raise IndexError('Position '+pos+' incorrecte')
        self._fils[pos]=a

    def __iter__(self) :
        """ Itère sur les fils. Si un fils vaut 'None' il est ignoré """
        for l in self._fils :
            if l!= None :
                yield l
    def lesfils(self) :
        return self._fils
    def __getitem__(self,i) :
        """ Renvoie une référence vers le fils numéro i
        Exemple :
        a=Arbre((4,5,(6,7,8)))
        b=a[1]
        print(b)
        >>> (6-(7,8))

        Lève IndexError si l'indice es incorrect
        """
        if i<0 : i<len(self._fils)-i
        if i not in range(len(self._fils)) :
            raise IndexError('Pas de fils '+str(i))
        return self._fils[i]

    def __setitem__(self,i,v) :
        """ Modifie le fils numéro i s'il existe et l'ajoute sinon
        """
        if i<0 : i<len(self._fils)-i
        if i<0 : raise IndexError('Pas de fils '+str(i))
        while len(self._fils)<=i : self._fils.append(None)
        if v.__class__==self.__class__ :
            self._fils[i]=v
        else :
            # Ci-dessous : à retenir, appelle Arbre(v) ou ArbreBinaire(v)
            # selon le type de self
            self._fils[i]=self.__class__(v)

    def __str__(self) :
        """ Renvoie une représentation lisible de l'objet sous
        forme de chaîne de caractères
        """
        s=[]
        for l in self._fils :
            if l==None : s.append('')
            else :s.append(str(l))
        s=",".join(s)
        if s!="" : return "("+str(self.__label)+"-("+s+"))"
        else : return str(self.__label)

    def __len__(self) :
        """ Renvoie le nombre de fils (différents de None) """
        return len([f for f in self._fils if f !=None])

    def __repr__(self) :
        if len(self._fils)==0 : return self.__class__.__name__+"("+repr(self.racine)+")"
        f=[]
        for l in self._fils :
            if l==None : f.append(repr(None))
            else :
                f.append(repr(l))
            pass
        return self.__class__.__name__+"(("+repr(self.racine)+","+",".join(f)+"))"

    def _innerdot(self) :
        stri=""
        for a in self :
            stri+="{0} -> {1} [label=\"\"];\n".format(id(self),id(a))
        col="white"
        infos=str(self.racine)
        attr="fillcolor=\"#888888ff\""
        stri+='\"{label}\"  [label=\"{infos}\", style = filled, peripheries = 1, \
                fillcolor = {col}, color = black];\n'.format(label=id(self),infos=infos,col=col)
        for a in self :
            stri+=a._innerdot()
        return stri

    def dot(self,printinfos=True) :
        """ Crée une chaîne de caractère contenant une
        description de l'arbre pour le programme dot (graphviz)
        """
        return "digraph g {\n"+self._innerdot()+"}\n"

    def save(self,filename='graphout.png') :
        """ Sauvegarde une image de l'abre dans un fichier (Graphviz nécessaire)"""
        try :
            pipe=subprocess.Popen(['dot','-Tpng','-o',filename],stdin=subprocess.PIPE)
            pipe.stdin.write(self.dot().encode('ascii') + b'\n')
            pipe.stdin.close()
            pipe.wait()
        except OSError as e :
            print("Impossible de Tracer le graphe...")

    def view(self) :
        """ Affiche l'arbre (Graphviz et ImageMagick nécessaires)
        """
        try :
            pipe=subprocess.Popen(['dot','-Tpng'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            pipe.stdin.write(self.dot().encode('ascii') + b'\n')
            pipe.stdin.close()
            l=pipe.stdout.read()
            pipe.wait()
            pipe=subprocess.Popen(['display'],stdin=subprocess.PIPE)
            pipe.stdin.write(l)
            pipe.stdin.close()
        except OSError as e :
            print("Impossible de Tracer le graphe...")



class ArbreBinaire(Arbre) :
    def __init__(self, first, **kwargs) :
        """
        Crée un arbre binaire à partir
        1) de la même façon qu'on crée un Arbre
        2) à partir d'un Arbre
        """
        if isinstance(first,Arbre) :
            l=[]
            for f in first._fils :
                if f==None : l.append(None)
                else : l.append(ArbreBinaire(f))
            Arbre.__init__(self,first.racine,fils=l[0:2])
        else :
            a=Arbre(first,**kwargs)
            self.__init__(a)

    def dot(self,printinfos=True) :
        """ Crée une chaîne de caractère contenant une
        description de l'arbre pour le programme dot (graphviz)
        Les fils sont ici ordonnés...
        """
        return 'digraph g {graph[ordering="out"];\n'+self._innerdot()+"}\n"

    @property
    def fg(self) :
        "Le fils gauche"
        return self._fils[0] if len(self._fils)>0  else None
    @fg.setter
    def fg(self,arb) :
        self.__setitem__(0,arb)

    @property
    def fd(self) :
        "Le fils droit"
        return self._fils[1] if len(self._fils)>0  else None
    @fd.setter
    def fd(self,arb) :
        self.__setitem__(1,arb)


    def _fg(self) :
        """ Référence vers le sous arbre gauche """
        return self._fils[0] if len(self._fils)>0  else None
    def _fd(self) :
        """ Référence vers le sous arbre droit """
        return self._fils[1] if len(self._fils)>1  else None
    def ajoute(self,a) :
        """ Ajoute l'arbre a comme nouveau fils de la racine
        (en fin de liste)
        """
        if len(self._fils)<2 : Arbre.ajoute(self,a)
        else : raise RuntimeError('Pas plus de deux fils pour un arbre binaire')

if __name__=='__main__' :
    ar=Arbre((10,1,(4,2,5,6,7),6,(13,10,11,4),15))
    d=ArbreBinaire(4,fils=(ArbreBinaire(3),Arbre(7)))
    print(ar)
    print(d)
