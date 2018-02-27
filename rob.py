from env import Node, Edge, Graph, Environment
from random import randint
import math

class Ndij:
	def __init__(self,n):
		self.n=n
		self.f=math.inf
		self.j=None



class Robot:
	def __init__(self,startpos):
		self.actualpos=startpos
		self.possiblepos=self.actualpos.adj
	
	def newactualpos(self,p):
		self.actualpos=p
		self.possiblepos=self.actualpos.adj


	def printpossiblepos(self):
		print('possibles steps:', end=' ')
		for x in range(len(self.possiblepos)):
			print(self.possiblepos[x].pos,end=' ')
		print(end='\n')
		
	############# scelta random  ########
	def randomnextstep(self):
		p=self.possiblepos[randint(0,len(self.possiblepos)-1)]
		self.newactualpos(p)
		
	def randomsteps(self,ns):
		for x in range(ns):
			print('step ',x+1)
			print('robot in:',self.actualpos.pos)
			self.printpossiblepos()
			self.randomnextstep()
			
	########## 
	
	def listnodesdij(self,ln):
		l=[]
		for x in range(len(ln)):
			temp=Ndij(ln[x])
			l.append(temp)
		return l
		
	def findnodedij(self,n,ln):
		for x in range(len(ln)):
			if n.pos== ln[x].n.pos :
				return ln[x]
		return None
	
	def findnodelistdij(self,n,ln):
		for x in range(len(ln)):
			if n.n.pos== ln[x].n.pos :
				return ln[x]
		return None
	
	def minf(self,ln):
		i=-1
		fi=math.inf
		for x in range(len(ln)):
			if ln[x].f < fi :
				i=x
				fi=ln[x].f
		return ln[i]
	
	def fpath(self,n,f,ln):
		aux=self.findnodedij(n.j,ln)
		if aux.j!=n.j :
			for x in range(len(ln)):
				if n.j==ln[x].n :
					f=f+ln[x].f
		return f
			
			
	def pathdij(self,s,t,g):
		if not t:
			return s
		else:
			mf=self.minf(t)
			s.append(mf)
			t.remove(mf)			
			for x in range(len(t)):
				if g.existedge(mf.n,t[x].n):
					jold=t[x].j
					t[x].j=mf.n
					temp=g.getedge(mf.n,t[x].n)
					f1=self.fpath(t[x],temp.w,s)
					if t[x].f > f1:
						t[x].f=self.fpath(t[x],temp.w,s)
					else:
						t[x].j=jold
			return self.pathdij(s,t,g)
	
	def minpathnodetonode(self,n,ld,ln):
		aux=self.findnodedij(n,ld)
		ln.append(aux)
		while aux.f!=0:
			for x in range(len(ld)):
				if ld[x].n==aux.j:
					ln.append(ld[x])
					aux=ld[x]
					break
		if aux not in ln:
			ln.append(aux)
		return ln
	
	def dijkstra(self,n1,n2,g):
		print(n1.pos)
		print(n2.pos)
		s=[]
		t=self.listnodesdij(g.nodes)
		for x in range(len(t)):
			if t[x].n.pos==n1.pos :
				t[x].f=0
				t[x].j=t[x].n
				break
		d=self.pathdij(s,t,g)
		
		for x in range(len(d)):							#
			print(d[x].n.pos,'->',d[x].f,end=' ')	 	#
		print()    										#
		s=[]
		s=self.minpathnodetonode(n2,d,s)
		s.reverse()
		return s
		
	
	############ scelta tra importanza #######
	
	

env=Environment(file=1)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
n1=env.g.nodes[randint(0,len(env.g.nodes)-1)]
r=Robot(n)
#r.randomsteps(1)
d=r.dijkstra(n,n1,env.g)
