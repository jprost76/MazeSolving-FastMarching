
import numpy as np
from numpy.linalg import norm
from matplotlib import pyplot as plt
from classMap import DistanceMap
from scipy import interpolate


#%% calcul de la fonction distance T
F = np.ones((50,50))
F[1,0:47] = 100
F[5,0:15] = 100
F[5:40,20] = 100
F[5,20:43] = 100
F[1:46,47] = 100
F[40,20:44] = 100
F[5:47,15] = 100
F[46,15:48] = 100
F[5:40,43] = 100

plt.figure()
plt.gray()
plt.imshow(F,interpolation='nearest')  

p0 = np.array((3,2))
m = DistanceMap([p0],F)
m.calculerDistance()

T = m.distanceMap()
plt.plasma()
plt.figure()
plt.imshow(T,interpolation='nearest')
     
#%% calcul de la geodesic en utilisant la descente du gradient
     
gradT = np.gradient(T)

# pas de la méthode du gradient
h = 0.1

#point de départ
p = np.array((44,45))

#courbe
mu = []

while (norm(p-p0,2)>h):
    mu.append(p)
    gradTp = np.array((gradT[0][p[0],p[1]],gradT[1][p[0],p[1]]))
    p = p - gradTp/norm(gradTp,2)
    
#%%

x = [p[1] for p in mu]
y = [p[0] for p in mu]
fig = plt.figure()
plt.hold('true')
ax = fig.add_subplot(111)
ax.imshow(F,interpolation='nearest')  
ax.scatter(x,y,c='r')
plt.show()

#%%

X = np.arange(T.shape[1])
Y = np.arange(T.shape[0])

#interpolation de T
T_inter = interpolate.RectBivariateSpline(Y,X,T)

#%%

h = 0.1;

#point de départ
p = np.array((44,45))

#courbe
mu = []

it=0;
while ((norm(p-p0,2)>h) & (it<10)):
    mu.append(p)
    gradTpx = T_inter(p[0],p[1],dx=1)[0,0]
    gradTpy = T_inter(p[0],p[1],dy=1)[0,0]
    gradTp = np.array((gradTpy,gradTpx))
    p = p - gradTp/norm(gradTp,2)
    it = it+1
    
x = [p[1] for p in mu]
y = [p[0] for p in mu]
fig = plt.figure(figsize=(10,10))
plt.hold('true')
ax = fig.add_subplot(111)
ax.imshow(T,interpolation='nearest')  
ax.scatter(x,y,c='r')
plt.show()