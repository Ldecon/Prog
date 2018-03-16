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
		self.actualpos.passcount=self.actualpos.passcount+1
		self.possiblepos=self.actualpos.adj


	def printpossiblepos(self):
		print('possibles steps:', end=' ')
		for x in range(len(self.possiblepos)):
			print(self.possiblepos[x].pos,end=' ')
		print(end='\n')

	def resetcounts(self,g):
		for x in range(len(g.nodes)):
			g.nodes[x].passcount=0
			g.nodes[x].visitcount=0
		
			
	########## dijkstra  ########################################################################################
	
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
	
	
	
	############# scelta random  ########################################################################
	
	def updatevaluesn(self,n):
		n.passcount=n.passcount+1
		
	
	def updatevcount(self,n,t):
		n.visitcount=n.visitcount+1
		n.lastvisit=t
	
	def randomsteps(self,ns,g):    #numstep
		self.resetcounts(g)
		self.updatevaluesn(self.actualpos)
		self.updatevcount(self.actualpos,1)
		x=0
		while x <= ns:
			#print('step ',x+1)
			#print('robot in:',self.actualpos.pos)
			#self.printpossiblepos()
			next=g.nodes[randint(0,len(g.nodes)-1)]
			d=self.dijkstra(self.actualpos,next,g)
			d.pop(0)
			for y in range(len(d)):
				x=x+1
				if x >= ns:
					break
				r.actualpos=d[y].n
				self.updatevaluesn(self.actualpos)
				if d[y].n.pos == next.pos:
					x=x+1
					if x <= ns:
						self.updatevcount(self.actualpos,x+1)
	
	############ scelta tra importanza ######################################################################
	
	def nodeidleness(self,n,t):			#node, time
		return abs(t-n.lastvisit)
		

	
	
	def nextstep(self,n,t,g):			#node, time, graph
		v=0
		for x in range(len(g.nodes)):
			g.nodes[x].valueimp=g.nodes[x].imp * abs(self.nodeidleness(g.nodes[x],t)) 
			if g.nodes[x].valueimp > v :
				next=g.nodes[x]
				v=g.nodes[x].valueimp
		return next		
				
				
	def imppath(self,ns,g):      #numstep,graph
		self.resetcounts(g)
		self.updatevaluesn(self.actualpos)
		self.updatevcount(self.actualpos,1)
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
				self.updatevaluesn(self.actualpos)
				if d[y].n.pos == next.pos:
					x=x+1
					if x <= ns:
						self.updatevcount(self.actualpos,x+1)
					
					
	def listnamepos(self,ln):
		auspos=[]
		for x in range(len(ln)):
			if ln[x].imp==4:
				auspos.append('CR '+ln[x].pos)
			else:
				auspos.append(ln[x].pos)
		return auspos
				
	def stats(self,ns,g):
		aus=g.nodes.copy()
		ausvcount=[]
		auspcount=[]	
		print('Pass')
		for x in range(len(aus)):
			auspcount.append(aus[x].passcount)
			if aus[x].imp==4:
				print('crnode -> ',end='')
			print('Node:',aus[x].pos,'imp=',aus[x].imp,'visits:',aus[x].passcount, 'times',(aus[x].passcount/ns)*100,'%')
		print('Visits')
		for x in range(len(aus)):
			ausvcount.append(aus[x].visitcount)
			if aus[x].imp==4:
				print('crnode -> ',end='')
			print('Node:',aus[x].pos,'imp=',aus[x].imp,'visits:',aus[x].visitcount, 'times',(aus[x].visitcount/ns)*100,'%')
		return auspcount,ausvcount
	
	
	def plotbarpass(self,d,x,y):
		ls=range(len(x))
		plt.figure('Stats', figsize=(20, 12))
		plt.title('Nodes visits\' stats')
		for z in range(len(y)):
			plt.subplot(2,len(y)/2,z+1)
			plt.bar(ls,y[z], color='g')	
			plt.title(d[z])
			plt.xticks(ls,x,rotation='vertical')
			for i in range(len(ls)):
				if x[i][0]=='C':
					plt.bar(i,y[z][i],color='r',align='center')
		plt.show()	
		
		
		##################### imp norm ############################################################################
		
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
		self.resetcounts(g)
		self.updatevaluesn(self.actualpos)
		self.updatevcount(self.actualpos,1)
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
				self.updatevaluesn(self.actualpos)
				if d[y].n.pos == next.pos:
					x=x+1
					if x <= ns:
						self.updatevcount(self.actualpos,x+1)
				
		
	

#env=Environment(file=1)
env=Environment(20)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
n1=env.g.nodes[randint(0,len(env.g.nodes)-1)]
r=Robot(n)
env.g.printg()
env.g.printedges()
y=[]
d=['# Random Pass',' # imp*idleness Pass','# (imp/impmax)*(idleness/idlenessmax) Pass','# Random Visits','# imp*idleness Visits','# (imp/impmax)*(idleness/idlenessmax) Visits' ]
print('Mode: random')
r.randomsteps(500,env.g)
y1,y2=r.stats(500,env.g)
print()
#d=r.dijkstra(n,n1,env.g)
print('Mode: imp*idleness')
r.imppath(1000,env.g)
y3,y4=r.stats(1000,env.g)
print()
print('Mode: (imp/impmax)*(idleness/idlenessmax)')
r.impnormpath(1000,env.g)
y5,y6=r.stats(1000,env.g)
print()
y.append(y1)
y.append(y3)
y.append(y5)
y.append(y2)
y.append(y4)
y.append(y6)
r.plotbarpass(d,r.listnamepos(env.g.nodes),y)

