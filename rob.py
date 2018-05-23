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
	
	def dijkstra(self,n1,n2,g):							#(startnode,finishnode,graph)
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
		
		
	################## johnson #########################################################################
		
		
	def johnson(self,g):
		matjo=[[None for x in range(len(g.nodes))]for x in range(len(g.nodes))]
		for x in range(len(g.nodes)):
			print(x)
			for y in range(len(g.nodes)):
				d=self.dijkstra(g.nodes[x],g.nodes[y],g)
				d.pop(0)
				matjo[int(g.nodes[x].pos)-1][int(g.nodes[y].pos)-1]=d
		return matjo
		
	def printmatjo(self,m):
		for x in range(len(m[0])):
			print(x+1,': ',end="")
			for y in range(len(m[0])):
				print('[',end='')
				for z in range(len(m[x][y])):
					print(m[x][y][z].n.pos, end=' ')
				print(']',end=' ')
			print()
				
	
	############# scelta random  ########################################################################
	
	def updatevaluesn(self,n):
		n.passcount=n.passcount+1
		
	
	def updatevcount(self,n,t):
		n.visitcount=n.visitcount+1
		n.lastvisit=t
	
					
	def randomsteps(self,ns,g,m):			#numsteps,graph,matjo
		self.resetcounts(g)
		self.updatevaluesn(self.actualpos)
		self.updatevcount(self.actualpos,1)
		x=0
		while x <= ns:
			next=g.nodes[randint(0,len(g.nodes)-1)]
			d=m[int(self.actualpos.pos)-1][int(next.pos)-1]
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
			if x > len(g.nodes):
				break
			g.nodes[x].valueimp=g.nodes[x].imp * self.nodeidleness(g.nodes[x],t)
			if g.nodes[x].valueimp > v :
				next=g.nodes[x]
				v=g.nodes[x].valueimp
		
		return next		
				
				
	def imppath(self,ns,g,m):				#numsteps,graph,matjo
		self.resetcounts(g)
		self.updatevaluesn(self.actualpos)
		self.updatevcount(self.actualpos,1)
		x=0
		
		while x<ns:
			next=self.nextstep(r.actualpos,x+1,g)
			d=m[int(self.actualpos.pos)-1][int(next.pos)-1]
			for y in range(len(d)):				
				x=x+1
				if x >= ns:
					break
				self.actualpos=d[y].n
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
		
	def sumvisits(self,ln):
		sv=0
		for i in range(len(ln)):
			sv=sv+ln[i].visitcount
		return sv
	
	def sumpass(self,ln):
		sp=0
		for i in range(len(ln)):
			sp=sp+ln[i].passcount
		return sp
	
				
	def stats(self,ns,g):
		aus=g.nodes.copy()
		ausvcount=[]
		auspcount=[]	
		print('Pass')
		for x in range(len(aus)):
			auspcount.append(aus[x].passcount)
			if aus[x].imp==4:
				print('crnode -> ',end='')
			print('Node:',aus[x].pos,'imp=',aus[x].imp,'visits:',aus[x].passcount, 'times',(aus[x].passcount/self.sumpass(g.nodes))*100,'%')
		print('Visits')
		for x in range(len(aus)):
			ausvcount.append(aus[x].visitcount)
			if aus[x].imp==4:
				print('crnode -> ',end='')
			print('Node:',aus[x].pos,'imp=',aus[x].imp,'visits:',aus[x].visitcount, 'times',(aus[x].visitcount/self.sumvisits(g.nodes))*100,'%')
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
			if x > len(g.nodes):
				break
			if g.nodes[x].imp >= maximp:
				maximp=g.nodes[x].imp

		return maximp
	
	def nextstepnorm(self,n,t,g):
		maxidl=self.maxidleness(t,g)
		maximp=self.maximp(g)
		next=None
		v=0
		for x in range(len(g.nodes)):
			if x > len(g.nodes):
				break
			if ((g.nodes[x].imp/maximp)*(self.nodeidleness(g.nodes[x],t)/maxidl)) > v:
				next=g.nodes[x]
				v=(g.nodes[x].imp/maximp)*(self.nodeidleness(g.nodes[x],t)/maxidl)
		return next
			
	def impnormpath(self,ns,g,m):					#numsteps,graph,matjo
		self.resetcounts(g)
		self.updatevaluesn(self.actualpos)
		self.updatevcount(self.actualpos,1)
		x=0		
		while x<ns:
			next=self.nextstepnorm(r.actualpos,x+1,g)
			d=m[int(self.actualpos.pos)-1][int(next.pos)-1]
			for y in range(len(d)):			
				x=x+1
				if x >= ns:
					break
				self.actualpos=d[y].n
				#print('Step', x+1)
				#print('Robot in:', self.actualpos.pos)
				self.updatevaluesn(self.actualpos)
				if d[y].n.pos == next.pos:
					x=x+1
					if x <= ns:
						self.updatevcount(self.actualpos,x+1)
						
	
	
		######################### algorithm ################################
	
	def avgidl(self,n,t):					#media idleness nodo
		idl=0
		if n.visitcount != 0:
			idl=(((n.visitcount-1)*n.nidlavg)+(t-n.lastvisit))/n.visitcount
		return idl
		
	def setavgidln(self,n,t):
		n.nidlavg=self.avgidl(n,t)
	
	def avgidlg(self,g,t):					#media idleness grafo
		avg=0
		for x in range(len(g.nodes)):
			avg=avg+self.avgidl(g.nodes[x],t)
		avg=avg/len(g.nodes)
		return avg	
	
	def dist(self,n1,n2,g):					#distanza
		ew=g.getedge(n1,n2).w
		av=self.avgwg(g)
		if ew > av :
			return ew
		else:
			return av
			
		
	def avgwg(self,g):								#media pesi degli archi
		avg=0
		for x in range(len(g.edges)):
			avg=avg+g.edges[x].w
		avg=avg/len(g.edges)
		return avg
	
	def dt(self,n1,n2,g,v):					#deltat = dist(n1,n2)/velocità robot
		return self.dist(n1,n2,g) / v
		
	def tnext(self,t,n1,n2,g,v):					#expected time = t+dt
		return t + self.dt(n1,n2,g,v)
		
	def idlexp(self,t,n1,n2,g,v):					#expected idleness = tnext/tlastvis
		return self.tnext(t,n1,n2,g,v)-n1.lastvisit
	
	def nextstepidl(self,t,n,g):
		i=0
		aus=None
		for x in range(len(n.adj)):
		#	i=self.idlexp(t,n,n.adj[x],g,v) / self.dt(n,n.adj[x],g,v)
		#	if u < i:
		#		u=i
		#		aus=n.adj[x]
		#		print("più grande",aus.pos,"con",u)
			if n.adj[x].visitcount == 0:
				aus=n.adj[x]
				break
			else:
				if	i < t-n.adj[x].lastvisit:
					i=t-n.adj[x].lastvisit
					aus=n.adj[x]
		return aus
	
	def idlalg(self,ns,g):
		self.updatevcount(self.actualpos,1)
		self.setavgidln(self.actualpos,1)
		avgg=self.avgidlg(g,1)
		print("avgg=",avgg)
		x=1
		while x < ns:
			next=self.nextstepidl(x+1,self.actualpos,g)
			self.actualpos=next
			self.setavgidln(self.actualpos,x+1)
			avgg=self.avgidlg(g,x+1)
			print("avgg=",avgg)
			self.updatevcount(self.actualpos,x+1)
			print(self.actualpos.pos)
			x=x+1
			
	def nextstepidlimp(self,t,n,g):
		i=0
		aus=None
		for x in range(len(n.adj)):
			if i < n.adj[x].imp+(t-n.adj[x].lastvisit):
				i=n.adj[x].imp+(t-n.adj[x].lastvisit)
				aus=n.adj[x]
		return aus

	def idlimpalg(self,ns,g):
		self.updatevcount(self.actualpos,1)
		self.setavgidln(self.actualpos,1)
		avgg=self.avgidlg(g,1)
		print("avgg=",avgg)
		x=1
		while x < ns:
			next=self.nextstepidlimp(x+1,self.actualpos,g)
			self.actualpos=next
			self.setavgidln(self.actualpos,x+1)
			avgg=self.avgidlg(g,x+1)
			print("avgg=",avgg)
			self.updatevcount(self.actualpos,x+1)
			print(self.actualpos.pos)
			x=x+1
	
	def visprint(self,g):
		for x in range(len(g.nodes)):
			print('Node:',g.nodes[x].pos,'imp:',g.nodes[x].imp,'visits:',g.nodes[x].visitcount, 'idleness avg:',g.nodes[x].nidlavg)


		####################### earth mover's distance ###############################################
		
		
	def minsumpq(self,ln):
		sumpass=0
		sumvis=0
		for i in range(len(ln)):
			sumpass=sumpass+ln[i].passcount
			sumvis=sumvis+ln[i].visitcount
		if sumpass <= sumvis :
			return sumpass
		else:
			return sumvis
	
	def emd(self,ln):   			#listnode
		w=0
		for i in range(len(ln)):
			for j in range(len(ln)):
				d=abs(ln[i].passcount-ln[j].visitcount)
				if ln[i].passcount >= ln[j].visitcount :
					f=ln[j].visitcount
				else:
					f=ln[i].passcount
				w=w+(d*f)
		
		return w/self.minsumpq(ln)
		
		
		######################## simple histograms comparison ###############################
	
	def comp(self,ln):
		w=0
		for i in range(len(ln)):
			d=abs(ln[i].passcount-ln[i].visitcount)
			w=w+d
		return w
		
		
		
		
	
	
		
		
		
		

#env=Environment(file=1)
'''			#emd graphics
listemd=[]
listcomp=[]
for x in range(10):
	sumemd=0
	sumcomp=0
	for y in range(10):
		env=Environment(10,ed=x*0.1)
		n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
		n1=env.g.nodes[randint(0,len(env.g.nodes)-1)]	
		r=Robot(n)
		env.g.printg()	
		env.g.printedges()
		m=r.johnson(env.g)
		#r.printmatjo(m)
		y=[]
		#d=['# Random Pass',' # imp*idleness Pass','# (imp/impmax)*(idleness/idlenessmax) Pass','# Random Visits','# imp*idleness Visits','# (imp/impmax)*(idleness/idlenessmax) Visits' ]		#histogram
		print('Mode: random')
		r.randomsteps(10000,env.g,m)
		y1,y2=r.stats(10000,env.g)
		print()
		print('Mode: imp*idleness')
		r.imppath(10000,env.g,m)
		y3,y4=r.stats(10000,env.g)
		print()
		print('Mode: (imp/impmax)*(idleness/idlenessmax)')
		r.impnormpath(10000,env.g,m)
		y5,y6=r.stats(10000,env.g)
		print()
		sumemd=sumemd+r.emd(env.g.nodes)
		sumcomp=sumcomp+r.comp(env.g.nodes)
		#y.append(y1)		#histogram
		#y.append(y3)		#histogram
		#y.append(y5)		#histogram
		#y.append(y2)		#histogram
		#y.append(y4)		#histogram
		#y.append(y6)		#histogram
		#r.plotbarpass(d,r.listnamepos(env.g.nodes),y)			#histogram
		env.destroye()
		del env.g
		del env
	listemd.append(sumemd/10)
	listcomp.append(sumcomp/10)
print(listemd)
print()
print(listcomp)
plt.figure(1, figsize=(10,4))
plt.subplot(121)
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],listemd)
plt.xlabel('% edges')
plt.ylabel('emd values')
plt.title('emd')
plt.subplot(122)
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],listcomp)
plt.xlabel('% edges')
plt.ylabel('comp values')
plt.title('histograms comparison')
plt.show()
'''
env=Environment(20,ed=0.8)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
r=Robot(n)
env.g.printg()	
env.g.printedges()
print('Mode: er')
r.idlimpalg(10000,env.g)
#y3,y4=r.stats(10000,env.g)
r.visprint(env.g)
















