import matplotlib.pyplot as plt 
import scipy.misc
import matplotlib.mlab as mlab
import numpy as np
from scipy import signal
import math
from PIL import Image
import sys
if len(sys.argv)==1:
	print("Give image filename as relative path to the cloning directory!")
	sys.exit(1)
elif len(sys.argv)>2:
	print("only 1 image file will be processed per run of canny.py")

face = np.array(Image.open(sys.argv[1]).convert('L'))
m,n=face.shape

def gaussm(n,sig):
	sig=sig**2
	return np.array([[(1./(2*math.pi*sig))*math.exp(-(1./(2*sig))*(np.square(i-n)+np.square(j-n))) for j in range(2*n+1)] for i in range(2*n+1)])
def fun1(a):
	a=math.degrees(a)
	if a>(67.5):
		return 90
	elif (a<=67.5 and a>22.5):
		return 45
	elif (a<=22.5 and a>-22.5):
		return 0
	elif (a<=-22.5 and a>-67.5):
		return -45
	else: return -90
def fun2(a):
	if a<=10: return 0
	if (a>=10 and a<=40):
		return 80
	elif a>=40: return 255
def eval(a,b):
	if b==0. :return math.pi/2
	else: return math.atan((1.*a)/b)
cov1=(1./159)*np.array([[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]])
cov=gaussm(2,1.96)
# print(cov1)
# print(cov)
face=face.flatten()
face=np.array([int(i) for i in face])
face=face.reshape(m,n)
face1=signal.convolve2d(face,cov,boundary='symm',mode='same')

kx=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
ky=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
# print(face.shape)

gx=signal.convolve2d(face1,kx,boundary='symm',mode='same').flatten()
gy=signal.convolve2d(face1,ky,boundary='symm',mode='same').flatten()
g=np.sqrt(np.square(gx)+np.square(gy))
base=np.zeros((m,n))
theta=np.array([eval(i,j) for i,j in zip(-gx,gy)])
theta=theta.reshape(m,n)
g=g.reshape(m,n)
for i in range(m):
	for j in range(n):
		b=theta[i][j]
		a=g[i][j]
		if(i==0 or i==m-1 or j==0 or j==n-1):
			base[i][j]=0
		elif b==0:
			if(a>=g[i][j+1] and a>=g[i][j-1]):base[i][j]=a
			# if (j==0 and a>=theta[i][j+1])base[i][j]=a
			# elif (j==m-1 and a>=theta[i][j-1])base[i][j]=a
			# elif (j!=0 and j!=m-1 and a>=theta[i][j+1] a>=theta[i][j-1])base[i][j]=a

		elif b==45:
			if(a>=g[i-1][j+1] and a>=g[i+1][j-1]):base[i][j]=a

			# if((i==0 and j==0) or (i==m-1 and j==n-1))base[i][j]=a
			# elif (i==0 and j>0 and base[i][j]>=base[1][j-1])base[i][j]=a
			# elif (i==m-1 and j<n-1 and base[i][j]>=base[m-1][j+1])base[i][j]=a
			# elif (i==0 and j==n-1 and base[i][j]>=base[n-1][1])base[i][j]=a
		elif b==90:
			if(a>=g[i-1][j] and a>=g[i+1][j]):base[i][j]=a
		elif b==-45:
			if(a>=g[i+1][j+1] and a>=g[i-1][j-1]):base[i][j]=a
		else:
			if(a>=g[i-1][j] and a>=g[i+1][j]):base[i][j]=a
c=0
edge=np.array([[fun2(base[i][j]) for j in range(n)] for i in range (m)])
for i in range(m):
	for j in range(n):
		b=edge[i][j]
		if(i==0 or i==m-1 or j==0 or j==n-1):
			continue
		elif (b==80 and ((edge[i+1][j]==255 and edge[i-1][j]==255) or 
			(edge[i+1][j-1]==255 and edge[i-1][j+1]==255) or
			(edge[i+1][j+1]==255 and edge[i-1][j-1]==255) or
			(edge[i][j+1]==255 and edge[i][j-1]==255) )) :
			edge[i][j]=255
			c=c+1
		elif b==8.: edge[i][j]=0


import ntpath
from PIL import Image
result = Image.fromarray(np.array(edge).astype(np.uint8))
result.save("edges_"+ntpath.basename(sys.argv[1]))