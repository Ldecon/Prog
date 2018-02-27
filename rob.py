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
		
	def randomsteps(self,ns):    #numstep
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
		s=[]
		t=self.listnodesdij(g.nodes)
		for x in range(len(t)):
			if t[x].n.pos==n1.pos :
				t[x].f=0
				t[x].j=t[x].n
				break
		d=self.pathdij(s,t,g)
		
		#for x in range(len(d)):							#
		#	print(d[x].n.pos,'->',d[x].f,end=' ')	 	#
		#print()    										#
		s=[]
		s=self.minpathnodetonode(n2,d,s)
		s.reverse()
		return s

	
	############ scelta tra importanza #######
	
	def nodeidleness(self,n,t):			#node, time
		return t-n.lastvisit
		
	def updatevaluesn(self,n,t):
		n.cont=n.cont+1
		n.lastvisit=t
	
	
	def nextstep(self,n,t,g):			#node, time, graph
		v=0
		for x in range(len(g.nodes)):
			g.nodes[x].valueimp=g.nodes[x].imp * abs(self.nodeidleness(g.nodes[x],t)) 
			if g.nodes[x].valueimp > v :
				next=g.nodes[x]
				v=g.nodes[x].valueimp
		return next		
				
				
	def imppath(self,ns,g):      #numstep,graph
		self.updatevaluesn(self.actualpos,1)
		x=0
		print('Step', x+1)
		print('Robot in:', self.actualpos.pos)
		while x<=ns:
			next=self.nextstep(r.actualpos,x+1,g)
			d=self.dijkstra(r.actualpos,next,g)
			d.pop(0)
			for y in range(len(d)):				
				x=x+1
				if x >= ns:
					break
				r.actualpos=d[y].n
				print('Step', x+1)
				print('Robot in:', self.actualpos.pos)
				self.updatevaluesn(self.actualpos,x+1)
				
	def stats(self,ns,g):
		for x in range(len(g.nodes)):
			print('Node:',g.nodes[x].pos,'visits:',g.nodes[x].cont, 'times',(g.nodes[x].cont/ns)*100,'%')
		
		
		##################### imp norm
		
	def maxidleness(self,t,g):
		maxidl=0
		for x in range(len(g.nodes)):
			if abs(t-g.nodes[x].lastvisit) > maxidl:
				maxidl=t-g.nodes[x].lastvisit
		return maxidl
	
	def maximp(self,g):
		maximp=0
		for x in range(len(g.nodes)):
			if g.nodes[x].imp > maximp:
				maximp=g.nodes[x].imp
		return maximp
	
	def nextstepnorm(self,n,t,g):
		maxidl=self.maxidleness(t,g)
		maximp=self.maximp(g)
		v=0
		for x in range(len(g.nodes)):
			if ((g.nodes[x].imp/maximp)*(self.nodeidleness(g.nodes[x],t)/maxidl)) > v:
				next=g.nodes[x]
				v=(g.nodes[x].imp/maximp)*(self.nodeidleness(g.nodes[x],t)/maxidl)
		return next
			
	def impnormpath(self,ns,g):
		self.updatevaluesn(self.actualpos,1)
		x=0
		print('Step', x+1)
		print('Robot in:', self.actualpos.pos)
		while x<=ns:
			next=self.nextstepnorm(r.actualpos,x+1,g)
			d=self.dijkstra(r.actualpos,next,g)
			d.pop(0)
			for y in range(len(d)):				
				x=x+1
				if x >= ns:
					break
				r.actualpos=d[y].n
				print('Step', x+1)
				print('Robot in:', self.actualpos.pos)
				self.updatevaluesn(self.actualpos,x+1)
		
		
	

env=Environment(file=1)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
n1=env.g.nodes[randint(0,len(env.g.nodes)-1)]
r=Robot(n)
#r.randomsteps(1)
#d=r.dijkstra(n,n1,env.g)
#r.imppath(500,env.g)
r.impnormpath(1000,env.g)
r.stats(1000,env.g)
