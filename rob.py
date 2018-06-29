from env import Node, Edge, Graph, Environment
from random import randint
import matplotlib.pyplot as plt
import math
import os

class Ndij:
	def __init__(self,n):
		self.n=n
		self.f=math.inf
		self.j=None

class Observer:
	def __init__(self,obspos):
		self.obspos=obspos
		self.listidln=[]
		self.predictionlist=[]
		self.errlist=[]
		
		########### Nearest Neighbor ############
		
	def listelemeq(self, l):
		f=1
		for x in range(len(l)-1):
			if (l[x] - l[x+1]) != 0:
				f=0
				break
		return f
	
	def nn(self,k,listk):       #listk= sequenza di k elementi da confrontare
		guess=0
		#aus=[]												#debug
		if len(self.listidln) > k:
			eq=-1
			sumel=0
			for x in range(len(self.listidln)-k):
				subl=[]
				s=[]
				for y in range(k):
					subl.append(self.listidln[x+y])
					s.append(listk[y]-subl[y])
				if self.listelemeq(s)==1 :
					if eq < 0 or s[0] == 0 :
							eq=abs(s[0])
			#				aus=subl.copy()				#debug
							guess=self.listidln[x+k]		#differenza elemento per elemento, se differenza costante, il numero da indovinare sarà crescente/decrescente rispetto ai precendenti	
					else:
						if eq < 0 or eq > abs(s[0]): 
							eq=abs(s[0])
			#				aus=subl.copy()				#debug
							guess=self.listidln[x+k]+s[0]
				else:
					sumel=0
					for z in range(len(s)):
						sumel=sumel+s[z]
					if  eq < 0 or eq > abs(sumel):
			#			aus=subl.copy()					#debug
						eq=abs(sumel)
						guess=self.listidln[x+k]
					
				
		else:
			print('not enough elements')
			return None
		#print('lista da cercare:',listk,'aus=',aus)		#debug
		#print('scelto:',guess)								#debug
		return guess
	
		def __del__(self):
			del self

class Robot:
	def __init__(self,startpos):
		self.actualpos=startpos
		self.possiblepos=self.actualpos.adj
		
	def __del__(self):
		del self
	
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
						
	
	
		######################### utility function ################################
	
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
			
	def nextstepidlimp(self,t,n,g):
		u=0
		aus=None
		for x in range(len(n.adj)):
			i=((t-n.adj[x].lastvisit)*n.adj[x].imp)/g.getedge(n,n.adj[x]).w				#u(v)= (idl(v) * imp(v)) / d(v) 
			if u < i:
				u=i
				aus=n.adj[x]
		return aus

	def utidlimp(self,ns,g,o,k):
		obscountidl=0
		self.updatevcount(self.actualpos,1)
		self.setavgidln(self.actualpos,1)
		avgg=self.avgidlg(g,1)
		#print("avgg=",avgg)
		x=1
		lk=[]
		prediction=None
		flag=0
		while x < ns:
			next=self.nextstepidlimp(x+1,self.actualpos,g)
			distedg=g.getedge(self.actualpos,next).w
			self.actualpos=next
			obscountidl=obscountidl+1
			self.setavgidln(self.actualpos,x+1)
			avgg=self.avgidlg(g,x+1)
			#print("avgg=",avgg)
			self.updatevcount(self.actualpos,x+1)
			#print(self.actualpos.pos)
				
			if len(o.listidln) > k and flag==0:							#guessing
				flag=1
				lk=[] 											#	
				for y in range(k):								#
					lk.append(o.listidln[len(o.listidln)-k+y])	#
				prediction=o.nn(k,lk)							#
																#
				
				

			
			if self.actualpos == o.obspos:		
				o.listidln.append(obscountidl)
				if len(o.listidln) > k+1:
					#if obscountidl == prediction:
					#		print(obscountidl,' = ',prediction,' predizione dell\'osservatore esatta')
					#else:
					#	print(obscountidl,' != ',prediction,' predizione dell\'osservatore sbagliata')
					o.errlist.append((obscountidl-prediction)**2)
					o.predictionlist.append(prediction)
				flag=0
				obscountidl=0
				
			
			x=x+int(distedg)
		
			
	
	def visprint(self,g):
		nvis=0
		for x in range(len(g.nodes)):
			nvis=nvis+g.nodes[x].visitcount
		for x in range(len(g.nodes)):
			print('Node:',g.nodes[x].pos,'imp:',g.nodes[x].imp,'visits:',g.nodes[x].visitcount, 'idleness avg:',g.nodes[x].nidlavg,' percentuale:',(g.nodes[x].visitcount/nvis)*100,'%')


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
		
		
		
		
	
	def logfile(self,g,name,nstep,nnodes,nedges,nprove,k,o):
		ncomp=name + '.txt'
		os.makedirs(os.path.dirname(ncomp), exist_ok=True)
		f=open(ncomp,"w")
		f.write('Logfile\n')
		f.write(str(nstep))
		f.write(' Steps con ')
		f.write(str(nnodes))
		f.write(' Nodi al ')
		f.write(str(nedges*100))
		f.write('% di archi -')
		f.write('Prova numero ')
		f.write(str(nprove))
		f.write(' k= ')
		f.write(str(k))
		f.write('\n\nStruttura grafo\n\n')
		for a in g.matnodes:
			x=g.getnode(a)
			f.write(x.pos)
			f.write(', coord=(')
			f.write(str(x.cx))
			f.write(',')
			f.write(str(x.cy))
			f.write(') i=')
			f.write(str(x.imp))
			f.write(':')
			for n in x.adj:
				f.write(' ')
				f.write(n.pos)
			f.write('\n')
		for x in range(len(g.edges)):
			f.write('[')
			f.write(str(g.edges[x].n1.pos))
			f.write(',')
			f.write(str(g.edges[x].n2.pos))
			f.write(', w=')
			f.write(str(g.edges[x].w))
			f.write(']\n')
		f.write('\n\nVisite grafo\n\n')
		for x in range(len(g.nodes)):
			f.write('Node: ')
			f.write(str(g.nodes[x].pos))
			f.write(' imp: ')
			f.write(str(g.nodes[x].imp))
			f.write(' visits: ')
			f.write(str(g.nodes[x].visitcount))
			f.write(' idleness avg: ')
			f.write(str(g.nodes[x].nidlavg))
			f.write(' percentuale: ')
			nvis=0
			for y in range(len(g.nodes)):
				nvis=nvis+g.nodes[y].visitcount
			f.write(str((g.nodes[x].visitcount/nvis)*100))
			f.write('%')
			f.write('\n')
		
		f.write('\nOsservatore\n\n')
		f.write('Nodo osservato: ')
		f.write(str(o.obspos.pos))
		f.write('\nLista idleness\n[ ')
		for x in range(len(o.listidln)):
			f.write(' ')
			f.write(str(o.listidln[x]))
			f.write(' ')
		f.write(']')
		f.write('\nLista previsioni\n[ ')
		for x in range(len(o.predictionlist)):
			f.write(' ')
			f.write(str(o.predictionlist[x]))
			f.write(' ')
		f.write(']')
		f.write('\nLista errore previsioni\n[ ')
		for x in range(len(o.errlist)):
			f.write(' ')
			f.write(str(o.errlist[x]))
			f.write(' ')
		f.write(']')
		f.close()
		
	
				
				
				
		
		

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


steps=[50000,100000,150000]
for s in range(len(steps)):
	names= 'log/' + str(steps[s]) + 'steps/'
	for nnod in range(10):#10
		namen=names + str((nnod+1)*10) + 'nodi/'
		for nedg in range(11):#11
			namee= namen + str(nedg*10) + '% archi/'	
			k=3
			listk=[]
			while k < 11:#11
				namek= namee + 'k'+ str(k) + '/'
				listkerr=[]				
				for x in range(20):
					namet = namek + 'Test' + str(x)
					env=Environment((nnod+1)*10,g=Graph(), ed=nedg*0.1)
					n=env.g.nodes[randint(0,len(env.g.nodes)-1)]	
					r=Robot(n)
					o=Observer(env.g.nodes[randint(0,len(env.g.nodes)-1)])
					env.g.printg()	
					env.g.printedges()
					print('Mode: ut')
					r.utidlimp(5000,env.g,o,5)	
					#y3,y4=r.stats(10000,env.g)
					r.visprint(env.g)
					print('num el oss=',len(o.listidln),'osservatore: (nodo:',o.obspos.pos,') ', o.listidln)
					
					r.logfile(env.g,namet,steps[s],(nnod+1)*10,nedg*0.1,x,k,o)
					plt.figure('Observer', figsize=(20,4))
					plt.subplot(121)
					plt.plot(o.listidln)
					plt.xlabel('t')
					plt.ylabel('idleness')
					plt.title('Idleness observed')
					plt.subplot(122)
					plt.plot(o.errlist)
					plt.title('Observer error prediction')
					plt.ylabel('Square error')
					plt.xlabel('t')
					plt.savefig(namet)
					#plt.show()
					plt.close()
					se=0
					aus=[]
					if len(o.errlist) > 2: 
						z=2
						aus.append(o.errlist[z])
						if len(o.errlist) >= 12:
							z=z+(len(o.errlist)/10)
							while int(z) < len(o.errlist):
								aus.append(o.errlist[int(z)])
								z=z+z
						else:
							z=z+1
							while z < len(o.errlist):
								aus.append(o.errlist[z])
								z=z+z			
								
						for y in range(len(aus)):
							se=se+aus[y]
						#print('gradnezza aus:', len(aus))
						listkerr.append(se/len(aus))
					env.destroye()
					del env.g
					del env
					del r
					del o
				se=0
				for y in range(len(listkerr)):
					se=se+listkerr[y]
				listk.append(se/len(listkerr))
				k=k+1
			lisx=[]
			for x in range(len(listk)):
				lisx.append(x+3)
				
			plt.plot(lisx,listk)
			plt.xlabel('k')
			plt.ylabel('MSE')
			namg=namee + 'Grafico errore medio k' + str((nnod+1)*10) + 'nodi' + str(nedg*10) + 'archi'
			plt.title('Grafico errore medio k')
			plt.savefig(namg)
			plt.close()
			
	











