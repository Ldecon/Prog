from env import Node, Edge, Graph, Environment
from random import randint
import matplotlib.pyplot as plt
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
		self.actualpos.cont=self.actualpos.cont+1
		self.possiblepos=self.actualpos.adj


	def printpossiblepos(self):
		print('possibles steps:', end=' ')
		for x in range(len(self.possiblepos)):
			print(self.possiblepos[x].pos,end=' ')
		print(end='\n')

	def resetcont(self,g):
		for x in range(len(g.nodes)):
			g.nodes[x].cont=0
		
	############# scelta random  ########
	def randomnextstep(self):
		p=self.possiblepos[randint(0,len(self.possiblepos)-1)]
		self.newactualpos(p)
		
	def randomsteps(self,ns,g):    #numstep
		self.resetcont(g)
		self.actualpos.cont=self.actualpos.cont+1
		for x in range(ns):
			#print('step ',x+1)
			#print('robot in:',self.actualpos.pos)
			#self.printpossiblepos()
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
		return 
	
	def findnodelistdij(self,n,ln):
		for x in range(len(ln)):
			if n.n.pos== ln[x].n.pos :
				return ln[x]
		return 
	
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
		return abs(t-n.lastvisit)
		
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
		self.resetcont(g)
		self.updatevaluesn(self.actualpos,1)
		x=0
		#print('Step', x+1)
		#print('Robot in:', self.actualpos.pos)
		while x<=ns:
			next=self.nextstep(r.actualpos,x+1,g)
			d=self.dijkstra(r.actualpos,next,g)
			d.pop(0)
			for y in range(len(d)):				
				x=x+1
				if x >= ns:
					break
				r.actualpos=d[y].n
				#print('Step', x+1)
				#print('Robot in:', self.actualpos.pos)
				self.updatevaluesn(self.actualpos,x+1)
	
	def maxcont(self,t):
		n=0
		for x in range(len(t)):
			if t[x].cont >= n:
				n=t[x].cont
				a=t[x]
		return a
	
	def listnamepos(self,ln):
		auspos=[]
		for x in range(len(ln)):
			if ln[x].imp==4:
				auspos.append('CR '+ln[x].pos)
			else:
				auspos.append(ln[x].pos)
		return auspos
				
	def stats(self,ns,g):
		#temp=g.nodes.copy()
		aus=g.nodes.copy()
		#while temp:
		#	aus.append(self.maxcont(temp))
		#	for x in range(len(temp)):
		#		if  temp[x].pos == aus[len(aus)-1].pos:
		#			temp.pop(x)
		#			break
		ls=range(len(aus))
		auspos=[]
		auscont=[]	
		for x in range(len(aus)):
			auscont.append(aus[x].cont)
			if aus[x].imp==4:
				auspos.append('CR '+aus[x].pos)
				print('crnode -> ',end='')
			else:
				auspos.append(aus[x].pos)
			print('Node:',aus[x].pos,'imp=',aus[x].imp,'visits:',aus[x].cont, 'times',(aus[x].cont/ns)*100,'%')
		return auscont
	
	def plotbar(self,d,x,y):
		ls=range(len(x))
		plt.figure('Stats', figsize=(20, 6))
		plt.title('Nodes visits\' stats')
		for z in range(len(y)):
			plt.subplot(1,len(y),z+1)
			plt.bar(ls,y[z], color='g')	
			plt.title(d[z])
			plt.xticks(ls,x,rotation='vertical')
			for i in range(len(ls)):
				if x[i][0]=='C':
					plt.bar(i,y[z][i],color='r',align='center')
		plt.show()	
		
		
		##################### imp norm
		
	def maxidleness(self,t,g):
		maxidl=0.0
		for x in range(len(g.nodes)):
			if abs(t-g.nodes[x].lastvisit) > maxidl:
				maxidl=abs(t-g.nodes[x].lastvisit)
		return maxidl
	
	def maximp(self,g):
		maximp=0.0
		for x in range(len(g.nodes)):
			if g.nodes[x].imp > maximp:
				maximp=g.nodes[x].imp
		return maximp
	
	def nextstepnorm(self,n,t,g):
		maxidl=self.maxidleness(t,g)
		maximp=self.maximp(g)
		next=None
		v=0
		for x in range(len(g.nodes)):
			if ((g.nodes[x].imp/maximp)*(self.nodeidleness(g.nodes[x],t)/maxidl)) > v:
				next=g.nodes[x]
				v=(g.nodes[x].imp/maximp)*(self.nodeidleness(g.nodes[x],t)/maxidl)
		return next
			
	def impnormpath(self,ns,g):
		self.resetcont(g)
		self.updatevaluesn(self.actualpos,1)
		x=0
		#print('Step', x+1)
		#print('Robot in:', self.actualpos.pos)
		while x<=ns:
			next=self.nextstepnorm(r.actualpos,x+1,g)
			d=self.dijkstra(r.actualpos,next,g)
			d.pop(0)
			for y in range(len(d)):				
				x=x+1
				if x >= ns:
					break
				r.actualpos=d[y].n
				#print('Step', x+1)
				#print('Robot in:', self.actualpos.pos)
				self.updatevaluesn(self.actualpos,x+1)
		
		
	

#env=Environment(file=1)
env=Environment(20)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
n1=env.g.nodes[randint(0,len(env.g.nodes)-1)]
r=Robot(n)
env.g.printg()
env.g.printedges()
y=[]
d=['Random','imp*idleness','(imp/impmax)*(idleness/idlenessmax)']
print('Mode: random')
r.randomsteps(500,env.g)
y.append(r.stats(500,env.g))
print()
#d=r.dijkstra(n,n1,env.g)
print('Mode: imp*idleness')
r.imppath(1000,env.g)
y.append(r.stats(1000,env.g))
print()
print('Mode: (imp/impmax)*(idleness/idlenessmax)')
r.impnormpath(1000,env.g)
y.append(r.stats(1000,env.g))
print()
r.plotbar(d,r.listnamepos(env.g.nodes),y)

