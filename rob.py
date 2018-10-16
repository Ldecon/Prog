from env import Node, Edge, Graph, Environment
from random import randint, random
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
		self.atklist=[]
		self.erratklist=[]
		self.errnotatklist=[]
		
	def resetobslists(self):
		self.listidln=[]
		self.predictionlist=[]
		self.errlist=[]
		self.atklist=[]
		self.erratklist=[]
		self.errnotatklist=[]
		
		
	def __del__(self):
		del self.obspos
		del self.listidln
		del self.predictionlist
		del self.errlist
		del self.atklist
		del self.erratklist
		del self.errnotatklist
		del self
	
			
		########### Nearest Neighbor ############
		
	def listelemeq(self, l):
		f=1
		for x in range(len(l)-1):
			if (l[x] - l[x+1]) != 0:
				f=0
				break
		return f

	def numpredex(self):	   			#numero elemento esatto della predizione (primo elemento parte da 0)
		s=0
		if len(self.errlist) > 0:
			x=len(self.errlist)-1
			while self.errlist[x] == 0 and x > 0:
				s=s+1
				x=x-1
				
			if x >= 0:
				return len(self.errlist) -s
			else:
				return -1
			
	
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
							guess=self.listidln[x+k]			
					else:
						if eq < 0 or eq > abs(s[0]): 		#differenza elemento per elemento, se differenza costante, il numero da indovinare sarà crescente/decrescente rispetto ai precendenti
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
		
		
	def obsprediction(self,k,matsim):
		self.resetobslists()
		obscountidl=0
		lk=[]
		prediction=None
		flag=0
		for x in range(len(matsim[0])):
			
			if len(self.listidln) > k and flag==0:							#guessing
				flag=1														#
				lk=[] 														#	
				for y in range(k):											#
					lk.append(self.listidln[len(self.listidln)-k+y])		#
				prediction=self.nn(k,lk)									#
																			#
			if matsim[0][x]==self.obspos:
				self.listidln.append(obscountidl)
				if len(o.listidln) > k and flag==1:
					self.errlist.append((obscountidl-prediction)**2)		#calcolo errore predizione
					self.predictionlist.append(prediction)
					flag=0
				obscountidl=0
			else:
				obscountidl=obscountidl+1
				
	
	def obspossatk(self,k,matsim):
		self.resetobslists()
		obscountidl=0
		lk=[]
		prediction=None
		flag=0
		for x in range(len(matsim[0])):
			
			if len(self.listidln) > k and flag==0:							#guessing
				flag=1														#
				lk=[] 														#	
				for y in range(k):											#
					lk.append(self.listidln[len(self.listidln)-k+y])		#
				prediction=self.nn(k,lk)									#
																			#
			if matsim[0][x]==self.obspos:
				self.listidln.append(obscountidl)
				if len(self.listidln) > k and flag==1:
					self.errlist.append((obscountidl-prediction)**2)		#calcolo errore predizione
					self.predictionlist.append(prediction)
					if self.obspos.tatk < prediction:						#se tempo attacco < predizione allora possibile attacco(1)
						self.atklist.append(1)
					else:
						self.atklist.append(0)
					flag=0
				obscountidl=0
			else:
				obscountidl=obscountidl+1
				
				
	
	def vark(self,k):
		z=0
		x=len(self.errlist)-1
		if x >0: 
			if self.errlist[x] != 0:
				x=x-1
				f=0
				while x >= 0 and f==0:
					if self.errlist[x]==0:
						while x >=0 and self.errlist[x]==0:
							z=z+1
							x=x-1
						f=1	
					x=x-1

		if (x > 0) and (z > k):
			k=k+1
		return k				
			
	
	def obspredictionvar(self,k,matsim):				#predizione con k variabile adattabile in base alla finestra di confronto
		self.resetobslists()
		obscountidl=0
		lk=[]
		prediction=None
		flag=0
		for x in range(len(matsim[0])):
			k=self.vark(k)
			if len(self.listidln) > k and flag==0:							#guessing
				flag=1														#
				lk=[] 														#	
				for y in range(k):											#
					lk.append(self.listidln[len(self.listidln)-k+y])		#
				prediction=self.nn(k,lk)									#
																			#
			if matsim[0][x]==self.obspos:
				self.listidln.append(obscountidl)
				if len(o.listidln) > k and flag==1:
					self.errlist.append((obscountidl-prediction)**2)		#calcolo errore predizione
					self.predictionlist.append(prediction)
					flag=0
				obscountidl=0
			else:
				obscountidl=obscountidl+1
	
	
	def obspossatkvark(self,k,matsim):						#tempo attacco con k variabile
		self.resetobslists()
		obscountidl=0
		lk=[]
		prediction=None
		flag=0
		for x in range(len(matsim[0])):
			k=self.vark(k)
			if len(self.listidln) > k and flag==0:							#guessing
				flag=1														#
				lk=[] 														#	
				for y in range(k):											#
					lk.append(self.listidln[len(self.listidln)-k+y])		#
				prediction=self.nn(k,lk)									#
																			#
			if matsim[0][x]==self.obspos:
				self.listidln.append(obscountidl)
				if len(self.listidln) > k and flag==1:
					self.errlist.append((obscountidl-prediction)**2)		#calcolo errore predizione
					self.predictionlist.append(prediction)
					if self.obspos.tatk < prediction:						#se tempo attacco < predizione allora possibile attacco(1)
						self.atklist.append(1)
					else:
						self.atklist.append(0)
					flag=0
				obscountidl=0
			else:
				obscountidl=obscountidl+1	
		return k

	def counterr(self,l):
		e=0
		for x in range(len(l)):
			if l[x]:
				e=e+1
		return e
	
			
	def logfileobs(self,f):
		f.write('\nOsservatore\n\n')
		f.write('Nodo osservato: ')
		f.write(str(self.obspos.pos))
		f.write('\nLista idleness\n[ ')
		for x in range(len(self.listidln)):
			f.write(' ')
			f.write(str(self.listidln[x]))
			f.write(' ')
		f.write('] elementi: '+str(len(self.listidln)))
	
	def logfileprev(self,f,k):
		f.write('\n k= ')
		f.write(str(k))
		f.write('\nLista previsioni\n[ ')
		for x in range(len(self.predictionlist)):
			f.write(' ')
			f.write(str(self.predictionlist[x]))
			f.write(' ')
		f.write('] elementi: '+str(len(self.predictionlist)))
		f.write('\nLista errore previsioni\n[ ')
		for x in range(len(self.errlist)):
			f.write(' ')
			f.write(str(self.errlist[x]))
			f.write(' ')
		f.write('] elementi: '+str(len(self.errlist)))
		f.write('\nNumero tentativi previsione esatta: ')
		f.write(str(self.numpredex()))
		f.write('\nLista possibili attacchi\n[')
		for x in range(len(self.atklist)):
			f.write(' ')
			f.write(str(self.atklist[x]))
			f.write(' ')
		f.write('] elementi: '+str(len(self.atklist)))
		f.write('\n n volte in attacco:' + str(self.counterr(self.atklist)))
		f.write('\nLista errori possibili attacchi\n[')
		for x in range(len(self.erratklist)):
			f.write(' ')
			f.write(str(self.erratklist[x]))
			f.write(' ')
		f.write('] elementi: '+str(len(self.erratklist)))
		f.write('\n n errori attacco:' + str(self.counterr(self.erratklist)))
		f.write('\nLista errori possibili NON attacchi\n[')
		for x in range(len(self.errnotatklist)):
			f.write(' ')
			f.write(str(self.errnotatklist[x]))
			f.write(' ')
		f.write('] elementi: '+str(len(self.errnotatklist)))
		f.write('\n n errori non attacco:' + str(self.counterr(self.errnotatklist)))
	

		
		

class Robot:
	def __init__(self,startpos):
		self.actualpos=startpos
		self.possiblepos=self.actualpos.adj
		
	def __del__(self):
		del self.actualpos
		del self.possiblepos
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
			g.nodes[x].lastvisit=0
			g.nodes[x].nidlavg=0
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
			i=((t-n.adj[x].lastvisit)*(n.adj[x].imp/n.adj[x].tatk))/g.getedge(n,n.adj[x]).w				#u(v)= (idl(v) * (imp(v)/tatk(v))) / d(v) 
			#i=((t-n.adj[x].lastvisit)*(n.adj[x].imp))/g.getedge(n,n.adj[x]).w
			if u < i:
				u=i
				aus=n.adj[x]
		return aus

	def utidlimp(self,ns,g):
		budget=0
		matsim=[[],[]]							#matrice simulazione [nodi che visita, tempo in budget]
		self.resetcounts(g)
		self.updatevcount(self.actualpos,1)
		self.setavgidln(self.actualpos,1)
		avgg=self.avgidlg(g,1)
		#print("avgg=",avgg)
		matsim[0].append(self.actualpos)
		matsim[1].append(budget)
		x=1

		while x < ns:
			next=self.nextstepidlimp(x+1,self.actualpos,g)
			distedg=g.getedge(self.actualpos,next).w
			self.actualpos=next
			
			self.setavgidln(self.actualpos,x+1)
			avgg=self.avgidlg(g,x+1)
			#print("avgg=",avgg)
			self.updatevcount(self.actualpos,x+1)
			#print(self.actualpos.pos)
			budget=budget+distedg
			matsim[0].append(self.actualpos)						
			matsim[1].append(budget)
			x=x+1
		return matsim
	
	############## ut epsilon ###########################
	
	def nextrandom(self,n):
		next=n.adj[randint(0,len(n.adj)-1)]
		return next
	
	def nextrandomv(self,n,g):
		next=g.getnode(n).adj[randint(0,len(g.getnode(n).adj)-1)]
		return next
	
	def utidlimpep(self,ns,g,ep):
		budget=0
		matsim=[[],[]]							#matrice simulazione [nodi che visita, tempo in budget]
		self.resetcounts(g)
		self.updatevcount(self.actualpos,1)
		self.setavgidln(self.actualpos,1)
		avgg=self.avgidlg(g,1)
		#print("avgg=",avgg)
		matsim[0].append(self.actualpos)
		matsim[1].append(budget)
		x=1

		while x < ns:
			r=randint(1,100)
			if r > ep:
				next=self.nextrandom(self.actualpos)
			else:
				next=self.nextstepidlimp(x+1,self.actualpos,g)
							#random choise
			distedg=g.getedge(self.actualpos,next).w
			self.actualpos=next
			self.setavgidln(self.actualpos,x+1)
			avgg=self.avgidlg(g,x+1)
			#print("avgg=",avgg)
			self.updatevcount(self.actualpos,x+1)
			#print(self.actualpos.pos)
			budget=budget+distedg
			matsim[0].append(self.actualpos)						
			matsim[1].append(budget)
			x=x+1
		return matsim
	
	
	def getvis(self, g):
		lvis=[]
		for x in range(len(g.nodes)):
			lvis.append(g.nodes[x].visitcount)
		return lvis
	
	def visprint(self,g):
		nvis=0
		for x in range(len(g.nodes)):
			nvis=nvis+g.nodes[x].visitcount
		for x in range(len(g.nodes)):
			print('Node:',g.nodes[x].pos,'imp:',g.nodes[x].imp,'visits:',g.nodes[x].visitcount, 'idleness avg:',g.nodes[x].nidlavg,' percentuale:',(g.nodes[x].visitcount/nvis)*100,'%')
			
	def simprint(self,ms):
		for x in range(len(ms[0])):
			print('n: ',ms[0][x].pos,' t: ',ms[1][x])


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
		
		
		
	def logfilerob(self,f,g,nstep,nnodes,nedges,nprove,ms,ep):		#file,graph,numsteps,numnodes,numedges,numtest,matrixsimulation,epsilon
		f.write('\n\nEPSILON= ' + str(ep)+ '\n')
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
		f.write('\nSimulazione:\n\n')
		for x in range(len(ms[0])):
			f.write('step:' + str(x) + ' -> ')
			f.write(' n: ')
			f.write(str(ms[0][x].pos))
			f.write(' t: ')
			f.write(str(ms[1][x]))
			f.write('\n')

############################################# virtual environment ########################
	def fact(self,n):
		f=1
		for x in range(n):
			f=f*x+1
		return f
	
	def existspantree(self,v,g):
		for x in range(len(v)-1):
			if g.eqgraph(v[x]):
				return 1
		return 0


	def spantree(self, gr, g, n, matfreq, d):		#nuovo ambiente, ambiente, ultimo nodo, matrice di frequenze, profondità					
		if gr.numnodes == g.numnodes:
			return
		else:
			l=[]
			for x in range(len(g.getnode(n).adj)):
				if gr.getnode(g.getnode(n).adj[x])==None:
					l.append(g.getnode(n).adj[x])
			if not len(l):
				e=gr.getlistedge(n)
				if e[0].n1.pos == n.pos :
					n=e[0].n1
				else:
					n=e[0].n2
				self.spantree(gr,g,n, matfreq, d-1)
			else:
				lis=[]
				lad=[]		#lista frequenze nodi adiacenti
				m=0
				for y in range(len(l)):
					lad.append(matfreq[d][(int(l[y].pos)-1)])
				for y in range(len(lad)):
					m=lad[y]+m
				if not m:
					m=1 
				for y in range(len(lad)):
					lis.append(1-(lad[y]/m))
				m=0
				for y in range(len(lis)):
					m=lis[y]+m
				if not m:
					m=1
				for y in range(len(lis)):
					if y > 0:
						lis[y]=(lis[y]/m)+lis[y-1]
					else:
						lis[y]=lis[y]/m
				r=random()
				for y in range(len(lis)):
					m=y
					if r <= lis[y]:
						matfreq[d][(int(l[y].pos)-1)]=matfreq[d][(int(l[y].pos)-1)]+1
						break
				nn=g.getnode(l[y])
				gr.addvirtnode(Node(pos=nn.pos,imp=nn.imp,cx=nn.cx,cy=nn.cy,tatk=nn.tatk))
				gr.addedge(n,gr.nodes[len(gr.nodes)-1])
				n=gr.nodes[len(gr.nodes)-1]
				self.spantree(gr,g,n,matfreq,d+1)
		
		
	def mkvirtenv(self,g,v,matfreq):
		v.append(Graph())
		l=[]
		m=0
		for x in range(len(matfreq[0])):
			m=matfreq[0][x]+m
		if not m:
			m=1 
		for x in range(len(matfreq[0])):
			l.append(1-(matfreq[0][x]/m))
		m=0
		for x in range(len(l)):
			m=l[x]+m
		for x in range(len(l)):
			if x >0:
				l[x]=(l[x]/m)+l[x-1]
			else:
				l[x]=l[x]/m
		r=random()		
		for x in range(len(l)):
			m=x
			if r <= l[x]:
				matfreq[0][x]=matfreq[0][x]+1
				break
		n=g.getnodeint(x+1)
		v[len(v)-1].addvirtnode(Node(pos=n.pos,imp=n.imp,cx=n.cx,cy=n.cy,tatk=n.tatk))
		self.spantree(v[len(v)-1],g,v[len(v)-1].nodes[0],matfreq,1)
		if self.existspantree(v,v[len(v)-1]):
			v.pop(len(v)-1)
							

	
	def logvirtenv(f,v):	#file, array ambienti virtuali
		for x in range(len(v)):
			v[x].logfileenvvirt(f,x)
			f.write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
		f.write('numero ambienti virtuali=' + len(v))	
	
	def linage(self, age):			#p lineare
		t=100					#max age T=100
		p=0 						
		if age > t:
			p=1
		else:
			p=age/t
		return p 
	
	def expage(self,age):			#p esponenziale
		t=100				#max age T
		p=0
		if age > t:
			p=1
		else:
			p=(math.exp(age/21.71))/t
		return p
	
	def logage(self,age):			#p logaritmica
		t=100				#max age T
		p=0
		if age > t:
			p=1
		else:
			p=(math.log((age*1.5)+1))/6
		return p
	
	def utfunctvirt(self,ns,g,ep):			#numsteps, graph, epsilon)
		v=[]
		matfreq=[[0 for x in range(len(g.nodes))]for x in range(len(g.nodes))]
		self.mkvirtenv(g,v,matfreq)
		budget=0
		matsim=[[],[]]							#matrice simulazione [nodi che visita, tempo in budget]
		self.resetcounts(g)
		self.updatevcount(self.actualpos,1)
		self.setavgidln(self.actualpos,1)
		avgg=self.avgidlg(g,1)
		#print("avgg=",avgg)
		matsim[0].append(self.actualpos)
		matsim[1].append(budget)
		x=1
		age=0
		while x < ns:
			r=randint(1,100)
			if r > ep:
				next=self.nextrandomv(self.actualpos,v[len(v)-1])
				age=age+1
			else:
				next=self.nextstepidlimp(x+1,v[len(v)-1].getnode(self.actualpos),v[len(v)-1])
			pr=random()
			if pr > self.linage(age):				#drop event function
				age=age+1
			else:
				self.mkvirtenv(g,v,matfreq)
				age=0
							
			distedg=g.getedge(g.getnode(self.actualpos),next).w
			self.actualpos=next
			self.setavgidln(g.getnode(self.actualpos),x+1)
			avgg=self.avgidlg(g,x+1)
			#print("avgg=",avgg)
			self.updatevcount(g.getnode(self.actualpos),x+1)
			#print(self.actualpos.pos)
			budget=budget+distedg
			matsim[0].append(g.getnode(self.actualpos))						
			matsim[1].append(budget)
			x=x+1
		return matsim,v


nod=10
env=Environment(nod, ed=1)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
ob=env.g.nodes[randint(0,len(env.g.nodes)-1)]
#env.g.printgfile()
r=Robot(n)
o=Observer(ob)
v=[]
sim,v=r.utfunctvirt(10000,env.g,90)
env.g.printg()
env.g.printedges()
name= 'log/virt/testv'
os.makedirs(os.path.dirname(name), exist_ok=True)
f=open(name,"w")
env.logfileenv(f,env.g,10000,nod,1,1,sim)
env.logfileenvvirt(f,v)
k=3
o.obspossatkvark(k,sim)
o.erratklist=[]									#lista errore previsioni attacco
for i in range(len(o.atklist)):
	if (o.atklist[i] == 1) and (o.obspos.tatk >= o.listidln[i+k+1]):
		o.erratklist.append(1)
	else: 
		o.erratklist.append(0)								  
	if (o.atklist[i] == 0) and (o.obspos.tatk < o.listidln[i+k+1]):
		o.errnotatklist.append(1)
	else:
		o.errnotatklist.append(0)
o.logfileobs(f)
o.logfileprev(f,k)

plt.figure('Observer atk', figsize=(15,10))
plt.subplot(311)
plt.plot(o.atklist)
plt.xlabel('t')
plt.ylabel('Obs atk')
plt.title('Observer possible attack')
plt.subplot(312)
plt.plot(o.erratklist)
plt.title('Observer error prediction attack (1=error)')
plt.ylabel('Error atk')
plt.xlabel('t')
plt.subplot(313)
plt.plot(o.errnotatklist)
plt.title('Observer error prediction not attack (1=error)')
plt.ylabel('Error not atk')
plt.xlabel('t')
nameatk='log/virt/grafv'
os.makedirs(os.path.dirname(nameatk), exist_ok=True)
plt.savefig(nameatk)
#plt.show()
plt.close()
f.close()

'''
nod=25	
env=Environment(nod, ed=1)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
ob=env.g.nodes[randint(0,len(env.g.nodes)-1)]
env.g.printgfile()
r=Robot(n)
o=Observer(ob)
sim,v=r.utfunctvirt(10000,env.g,90,nod-2)
env.g.printg()
env.g.printedges()
name= 'log/virt/testv'
os.makedirs(os.path.dirname(name), exist_ok=True)
f=open(name,"w")
env.logfileenv(f,env.g,10000,nod,1,1,sim)
env.logfileenvvirt(f,v)
#env.g.printgfile()
k=3
o.obspossatkvark(k,sim)
o.erratklist=[]									#lista errore previsioni attacco
for i in range(len(o.atklist)):
	if (o.atklist[i] == 1) and (o.obspos.tatk >= o.listidln[i+k+1]):
		o.erratklist.append(1)
	else: 
		o.erratklist.append(0)								  
	if (o.atklist[i] == 0) and (o.obspos.tatk < o.listidln[i+k+1]):
		o.errnotatklist.append(1)
	else:
		o.errnotatklist.append(0)
o.logfileobs(f)
o.logfileprev(f,k)

plt.figure('Observer atk', figsize=(15,10))
plt.subplot(311)
plt.plot(o.atklist)
plt.xlabel('t')
plt.ylabel('Obs atk')
plt.title('Observer possible attack')
plt.subplot(312)
plt.plot(o.erratklist)
plt.title('Observer error prediction attack (1=error)')
plt.ylabel('Error atk')
plt.xlabel('t')
plt.subplot(313)
plt.plot(o.errnotatklist)
plt.title('Observer error prediction not attack (1=error)')
plt.ylabel('Error not atk')
plt.xlabel('t')
nameatk='log/virt/grafv'
os.makedirs(os.path.dirname(nameatk), exist_ok=True)
plt.savefig(nameatk)
#plt.show()
plt.close()
f.close()
'''		
'''
nod=10
env2=Environment(file=1)
n=env2.g.nodes[3]
ob=env2.g.nodes[4]
r2=Robot(n)
o2=Observer(ob)
sim=r2.utidlimpep(10000,env2.g,90)
env2.g.printg()
env2.g.printedges()
name= 'log/virt/test'
os.makedirs(os.path.dirname(name), exist_ok=True)
f=open(name,"w")
env2.logfileenv(f,env2.g,10000,nod,1,1,sim)
#env.g.printgfile()
k=3
o2.obspossatkvark(k,sim)
o2.erratklist=[]									#lista errore previsioni attacco
for i in range(len(o2.atklist)):
	if (o2.atklist[i] == 1) and (o2.obspos.tatk >= o2.listidln[i+k+1]):
		o2.erratklist.append(1)
	else: 
		o2.erratklist.append(0)								  
	if (o2.atklist[i] == 0) and (o2.obspos.tatk < o2.listidln[i+k+1]):
		o2.errnotatklist.append(1)
	else:
		o2.errnotatklist.append(0)
o2.logfileobs(f)
o2.logfileprev(f,k)

plt.figure('Observer atk', figsize=(15,10))
plt.subplot(311)
plt.plot(o2.atklist)
plt.xlabel('t')
plt.ylabel('Obs atk')
plt.title('Observer possible attack')
plt.subplot(312)
plt.plot(o2.erratklist)
plt.title('Observer error prediction attack (1=error)')
plt.ylabel('Error atk')
plt.xlabel('t')
plt.subplot(313)
plt.plot(o2.errnotatklist)
plt.title('Observer error prediction not attack (1=error)')
plt.ylabel('Error not atk')
plt.xlabel('t')
nameatk='log/virt/graf'
os.makedirs(os.path.dirname(nameatk), exist_ok=True)
plt.savefig(nameatk)
#plt.show()
plt.close()		
f.close()
'''


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

 #NN k fisso, epsilon random e tatk

sim=None
steps=[10000]
'''
for s in range(len(steps)):
	names= 'log/' + str(steps[s]) + 'steps/'
	for nnod in range(5):#10 -> fino a 100nodi
		namen=names + str((nnod+1)*10) + 'nodi/'
		for nedg in range(11):#11 -> da 0 a 100% archi
			namee= namen + str(nedg*10) + 'densità archi/'	
			for x in range(10):
				namet = namee + 'Test' + str(x) +'/'
				env=Environment((nnod+1)*10,g=Graph(), ed=nedg*0.1)
				start=env.g.nodes[randint(0,len(env.g.nodes)-1)]
				env.g.printg()	
				env.g.printedges()
				print('Mode: utep')
				ncomp=namet + 'log' + str(x) + '.txt'
				os.makedirs(os.path.dirname(ncomp), exist_ok=True)
				f=open(ncomp,"w")
				env.logfileenv(f,env.g,steps[s],(nnod+1)*10,nedg*0.1,x,sim)
				obsnode=env.g.nodes[randint(0,len(env.g.nodes)-1)]
				
				for epsilon in range(11):
					listk=[]				#lista k media su massimo 10 punti
					listp=[]				#lista prima predizione su k
					listcompk=[]			#lista predizione media completa
					k=3
					r=Robot(start)
					ep=100-(epsilon*10)
					sim=r.utidlimpep(steps[s],env.g,ep)
					#y3,y4=r.stats(10000,env.g)
					r.visprint(env.g)
					r.simprint(sim)
					r.logfilerob(f,env.g,steps[s],(nnod+1)*10,nedg*0.1,x,sim,(epsilon*0.1))
					o=Observer(obsnode)
					
					nameep=namet + 'epsilon' +str(epsilon*10) + '/'
					os.makedirs(os.path.dirname(nameep), exist_ok=True)
					
					
					while k < 11:#11
						o.obspossatk(k,sim)
						o.erratklist=[]									#lista errore previsioni attacco
						for i in range(len(o.atklist)):
							if (o.atklist[i] == 1) and (o.obspos.tatk >= o.listidln[i+k+1]):
								o.erratklist.append(1)
							else: 
								o.erratklist.append(0)								  
							if (o.atklist[i] == 0) and (o.obspos.tatk < o.listidln[i+k+1]):
								o.errnotatklist.append(1)
							else:
								o.errnotatklist.append(0)
								
						if k==3:
							o.logfileobs(f)
						o.logfileprev(f,k)
						print('num el oss=',len(o.listidln),'osservatore: (nodo:',o.obspos.pos,') ', o.listidln)	
						
						
						lisv=r.getvis(env.g)
						lnn=r.listnamepos(env.g.nodes)
						ls=range(len(lnn))
						plt.figure('Visits',figsize=(20,4))
						plt.bar(ls,lisv,color='g')
						plt.xticks(ls,lnn,rotation='vertical')
						for i in range(len(ls)):
							if lnn[i][0]=='C':
								plt.bar(i,lisv[i],color='r',align='center')
						plt.title('Robot visits')
						plt.savefig(namet + 'visits ep' + str(epsilon*10))
						plt.close()
						
						plt.figure('Observer', figsize=(30,7))
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
						plt.savefig(nameep + 'k' + str(k) + 'epsilon' + str(epsilon*10))
						#plt.show()
						plt.close()
						
						
						plt.figure('Observer atk', figsize=(15,10))
						plt.subplot(311)
						plt.plot(o.atklist)
						plt.xlabel('t')
						plt.ylabel('Obs atk')
						plt.title('Observer possible attack')
						plt.subplot(312)
						plt.plot(o.erratklist)
						plt.title('Observer error prediction attack (1=error)')
						plt.ylabel('Error atk')
						plt.xlabel('t')
						plt.subplot(313)
						plt.plot(o.errnotatklist)
						plt.title('Observer error prediction not attack (1=error)')
						plt.ylabel('Error not atk')
						plt.xlabel('t')
						nameatk=nameep +'atk/'
						os.makedirs(os.path.dirname(nameatk), exist_ok=True)
						plt.savefig(nameatk + 'k' + str(k) + 'epsilon' + str(epsilon*10))
						#plt.show()
						plt.close()
						
						se=0
						sc=0
						aus=[]
						for y in range(len(o.errlist)):
							sc=sc+o.errlist[y]
						if len(o.errlist) > 0: 
							z=0
							aus.append(o.errlist[z])
							if len(o.errlist) > 10:
								z=z+(len(o.errlist)/10)
								while int(z) < len(o.errlist):
									aus.append(o.errlist[int(z)])
									z=z+z
							else:
								z=z+1
								while z < len(o.errlist):
									aus.append(o.errlist[z])
									z=z+z			
						else:
							z=0
							while z < len(o.errlist):
								aus.append(o.errlist[z])
								z=z+z
						if len(aus) > 0:		
							for y in range(len(aus)):
								se=se+aus[y]
							#print('gradnezza aus:', len(aus))
							listk.append(se/len(aus))
						if len(o.errlist) > 0:
							listcompk.append(sc/len(o.errlist))
						else:
							listcompk.append(-1)
						listp.append(o.numpredex())
						
						k=k+1
				
				
				
					lisx=[]
					for x in range(len(listk)):
						lisx.append(x+3)	
					plt.figure('prediction period (max 10 points)', figsize=(30,7))
					plt.subplot(121)
					plt.plot(lisx,listk)
					plt.xlabel('k')
					plt.ylabel('MSE')
					plt.title('Grafico errore medio k su massimo 10 punti osservati con epsilon' +str(epsilon*10))
					lisx=[]
					for x in range(k-3):
						lisx.append(x+3)				
					plt.subplot(122)
					plt.plot(lisx,listp)
					plt.xlabel('k')
					plt.ylabel('Period')
					plt.title('Prediction')
					namg=nameep + 'Grafico errore medio su 10 punti e periodo predizione '+ str((nnod+1)*10) + 'nodi' + str(nedg*10) + 'archi con epsilon' +str(epsilon*10)
					plt.savefig(namg)
					plt.close()
					
					
					
					
					lisx=[]
					for x in range(len(listcompk)):
						lisx.append(x+3)	
					plt.figure('complete prediction period', figsize=(30,7))
					plt.subplot(121)
					plt.plot(lisx,listcompk)
					plt.xlabel('k')
					plt.ylabel('MSE')
					plt.title('Grafico errore medio k su tutti i punti osservati con epsilon' + str(epsilon*10))
					lisx=[]
					for x in range(k-3):
						lisx.append(x+3)				
					plt.subplot(122)
					plt.plot(lisx,listp)
					plt.xlabel('k')
					plt.ylabel('Period')
					plt.title('Prediction')
					namg=nameep + 'Grafico errore medio e periodo predizione '+ str((nnod+1)*10) + 'nodi' + str(nedg*10) + 'archi con epsilon' + str(epsilon*10)
					plt.savefig(namg)
					plt.close()
					
					
					del r
					del o
				f.close()
				env.destroye()
				del env.g
				del env
				'''
'''ultimi test
for s in range(len(steps)):
	names= 'log/' + str(steps[s]) + 'steps/'
	nnod=2 #10 -> fino a 100nodi
	namen=names + str((nnod+1)*10) + 'nodi/'
	for nedg in range(11):#11 -> da 0 a 100% archi
		namee= namen + str(nedg*10) + 'densità archi/'	
		for x in range(10):
			namet = namee + 'Test' + str(x) +'/'
			env=Environment((nnod+1)*10,g=Graph(), ed=nedg*0.1)
			start=env.g.nodes[randint(0,len(env.g.nodes)-1)]
			env.g.printg()	
			env.g.printedges()
			print('Mode: utep')
			ncomp=namet + 'log' + str(x) + '.txt'
			os.makedirs(os.path.dirname(ncomp), exist_ok=True)
			f=open(ncomp,"w")
			env.logfileenv(f,env.g,steps[s],(nnod+1)*10,nedg*0.1,x,sim)
			obsnode=env.g.nodes[randint(0,len(env.g.nodes)-1)]		
			epsilon=0
			listk=[]				#lista k media su massimo 10 punti
			listp=[]				#lista prima predizione su k
			listcompk=[]			#lista predizione media completa
			k=3
			r=Robot(start)
			ep=100-(epsilon*10)
			sim=r.utidlimpep(steps[s],env.g,ep)
			#y3,y4=r.stats(10000,env.g)
			r.visprint(env.g)
			r.simprint(sim)
			r.logfilerob(f,env.g,steps[s],(nnod+1)*10,nedg*0.1,x,sim,(epsilon*0.1))
			o=Observer(obsnode)
					
			nameep=namet + 'epsilon' +str(epsilon*10) + '/'
			os.makedirs(os.path.dirname(nameep), exist_ok=True)
					
					
			while k < 11:#11
				o.obspossatk(k,sim)
				o.erratklist=[]									#lista errore previsioni attacco
				for i in range(len(o.atklist)):
					if (o.atklist[i] == 1) and (o.obspos.tatk >= o.listidln[i+k+1]):
						o.erratklist.append(1)
					else: 
						o.erratklist.append(0)								  
					if (o.atklist[i] == 0) and (o.obspos.tatk < o.listidln[i+k+1]):
						o.errnotatklist.append(1)
					else:
						o.errnotatklist.append(0)
						
				if k==3:
					o.logfileobs(f)
				o.logfileprev(f,k)
				print('num el oss=',len(o.listidln),'osservatore: (nodo:',o.obspos.pos,') ', o.listidln)	
						
						
				lisv=r.getvis(env.g)
				lnn=r.listnamepos(env.g.nodes)
				ls=range(len(lnn))
				plt.figure('Visits',figsize=(20,4))
				plt.bar(ls,lisv,color='g')
				plt.xticks(ls,lnn,rotation='vertical')
				for i in range(len(ls)):
					if lnn[i][0]=='C':
						plt.bar(i,lisv[i],color='r',align='center')
				plt.title('Robot visits')
				plt.savefig(namet + 'visits ep' + str(epsilon*10))
				plt.close()
						
				plt.figure('Observer', figsize=(30,7))
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
				plt.savefig(nameep + 'k' + str(k) + 'epsilon' + str(epsilon*10))
				#plt.show()
				plt.close()
						
						
				plt.figure('Observer atk', figsize=(15,10))
				plt.subplot(311)
				plt.plot(o.atklist)
				plt.xlabel('t')
				plt.ylabel('Obs atk')
				plt.title('Observer possible attack')
				plt.subplot(312)
				plt.plot(o.erratklist)
				plt.title('Observer error prediction attack (1=error)')
				plt.ylabel('Error atk')
				plt.xlabel('t')
				plt.subplot(313)
				plt.plot(o.errnotatklist)
				plt.title('Observer error prediction not attack (1=error)')
				plt.ylabel('Error not atk')
				plt.xlabel('t')
				nameatk=nameep +'atk/'
				os.makedirs(os.path.dirname(nameatk), exist_ok=True)
				plt.savefig(nameatk + 'k' + str(k) + 'epsilon' + str(epsilon*10))
				#plt.show()
				plt.close()
						
				se=0
				sc=0
				aus=[]
				for y in range(len(o.errlist)):
					sc=sc+o.errlist[y]
				if len(o.errlist) > 0: 
					z=0
					aus.append(o.errlist[z])
					if len(o.errlist) > 10:
						z=z+(len(o.errlist)/10)
						while int(z) < len(o.errlist):
							aus.append(o.errlist[int(z)])
							z=z+z
					else:
						z=z+1
						while z < len(o.errlist):
							aus.append(o.errlist[z])
							z=z+z			
				else:
					z=0
					while z < len(o.errlist):
						aus.append(o.errlist[z])
						z=z+z
				if len(aus) > 0:		
					for y in range(len(aus)):
						se=se+aus[y]
					#print('gradnezza aus:', len(aus))
					listk.append(se/len(aus))
				if len(o.errlist) > 0:
					listcompk.append(sc/len(o.errlist))
				else:
					listcompk.append(-1)
				listp.append(o.numpredex())
						
				k=k+1
				
				
				
			lisx=[]
			for x in range(len(listk)):
				lisx.append(x+3)	
			plt.figure('prediction period (max 10 points)', figsize=(30,7))
			plt.subplot(121)
			plt.plot(lisx,listk)
			plt.xlabel('k')
			plt.ylabel('MSE')
			plt.title('Grafico errore medio k su massimo 10 punti osservati con epsilon' +str(epsilon*10))
			lisx=[]
			for x in range(k-3):
				lisx.append(x+3)				
			plt.subplot(122)
			plt.plot(lisx,listp)
			plt.xlabel('k')
			plt.ylabel('Period')
			plt.title('Prediction')
			namg=nameep + 'Grafico errore medio su 10 punti e periodo predizione '+ str((nnod+1)*10) + 'nodi' + str(nedg*10) + 'archi con epsilon' +str(epsilon*10)
			plt.savefig(namg)
			plt.close()
					
					
					
					
			lisx=[]
			for x in range(len(listcompk)):
				lisx.append(x+3)	
			plt.figure('complete prediction period', figsize=(30,7))
			plt.subplot(121)
			plt.plot(lisx,listcompk)
			plt.xlabel('k')
			plt.ylabel('MSE')
			plt.title('Grafico errore medio k su tutti i punti osservati con epsilon' + str(epsilon*10))
			lisx=[]
			for x in range(k-3):
				lisx.append(x+3)				
			plt.subplot(122)
			plt.plot(lisx,listp)
			plt.xlabel('k')
			plt.ylabel('Period')
			plt.title('Prediction')
			namg=nameep + 'Grafico errore medio e periodo predizione '+ str((nnod+1)*10) + 'nodi' + str(nedg*10) + 'archi con epsilon' + str(epsilon*10)
			plt.savefig(namg)
			plt.close()
					
					
			del r
			del o
		f.close()
		env.destroye()
		del env.g
		del env
'''			
			
				
'''	test k variabile		
env=Environment(10,g=Graph(), ed=0)
start=env.g.nodes[randint(0,len(env.g.nodes)-1)]
env.g.printg()	
env.g.printedges()
print('Mode: utep')				
obsnode=env.g.nodes[randint(0,len(env.g.nodes)-1)]		
k=3
r=Robot(start)
ep=100
sim=r.utidlimpep(10000,env.g,ep)
#y3,y4=r.stats(10000,env.g)
r.visprint(env.g)
r.simprint(sim)	
o=Observer(obsnode)
o.obspredictionvar(k,sim)
print('num el oss=',len(o.listidln),'osservatore: (nodo:',o.obspos.pos,') ', o.listidln, '\nerrlist: [', o.errlist, ']')
plt.figure('Observer', figsize=(30,7))
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
plt.show()
plt.close()
'''
'''
 #NN k varaibile, epsilon random e tatk

sim=None
steps=[10000]
for s in range(len(steps)):
	names= 'log/' + str(steps[s]) + 'steps/'
	for nnod in range(5):#10 -> fino a 100nodi
		namen=names + str((nnod+1)*10) + 'nodi/'
		for nedg in range(11):#11 -> da 0 a 100% archi
			namee= namen + str(nedg*10) + 'densità archi/'	
			for x in range(10):
				namet = namee + 'Test' + str(x) +'/'
				env=Environment((nnod+1)*10,g=Graph(), ed=nedg*0.1)
				start=env.g.nodes[randint(0,len(env.g.nodes)-1)]
				env.g.printg()	
				env.g.printedges()
				print('Mode: utep')
				ncomp=namet + 'log' + str(x) + '.txt'
				os.makedirs(os.path.dirname(ncomp), exist_ok=True)
				f=open(ncomp,"w")
				env.logfileenv(f,env.g,steps[s],(nnod+1)*10,nedg*0.1,x,sim)
				obsnode=env.g.nodes[randint(0,len(env.g.nodes)-1)]
				
				for epsilon in range(11):
					k=3
					r=Robot(start)
					ep=100-(epsilon*10)
					sim=r.utidlimpep(steps[s],env.g,ep)
					#y3,y4=r.stats(10000,env.g)
					r.visprint(env.g)
					r.simprint(sim)
					r.logfilerob(f,env.g,steps[s],(nnod+1)*10,nedg*0.1,x,sim,(epsilon*0.1))
					o=Observer(obsnode)
					
					nameep=namet + 'epsilon' +str(epsilon*10) + '/'
					os.makedirs(os.path.dirname(nameep), exist_ok=True)
					
					k=o.obspossatkvark(k,sim)
					print('\n[')
					for x in range(len(o.errlist)):
						print (o.errlist[x], end=' ')
					print(']')
					o.erratklist=[]									#lista errore previsioni attacco
					for i in range(len(o.atklist)):
						if (o.atklist[i] == 1) and (o.obspos.tatk >= o.listidln[i+3+1]):
							o.erratklist.append(1)
						else: 
							o.erratklist.append(0)								  
						if (o.atklist[i] == 0) and (o.obspos.tatk < o.listidln[i+3+1]):
							o.errnotatklist.append(1)
						else:
							o.errnotatklist.append(0)
					
					o.logfileobs(f)
					o.logfileprev(f,k)
					print('num el oss=',len(o.listidln),'osservatore: (nodo:',o.obspos.pos,') ', o.listidln)	
						
						
					lisv=r.getvis(env.g)
					lnn=r.listnamepos(env.g.nodes)
					ls=range(len(lnn))
					plt.figure('Visits',figsize=(20,4))
					plt.bar(ls,lisv,color='g')
					plt.xticks(ls,lnn,rotation='vertical')
					for i in range(len(ls)):
						if lnn[i][0]=='C':
							plt.bar(i,lisv[i],color='r',align='center')
					plt.title('Robot visits')
					plt.savefig(namet + 'visits ep' + str(epsilon*10))
					plt.close()
						
					plt.figure('Observer', figsize=(30,7))
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
					plt.savefig(nameep + 'varkepsilon' + str(epsilon*10))
					#plt.show()
					plt.close()
						
						
					plt.figure('Observer atk', figsize=(15,10))
					plt.subplot(311)
					plt.plot(o.atklist)
					plt.xlabel('t')
					plt.ylabel('Obs atk')
					plt.title('Observer possible attack')
					plt.subplot(312)
					plt.plot(o.erratklist)
					plt.title('Observer error prediction attack (1=error)')
					plt.ylabel('Error atk')
					plt.xlabel('t')
					plt.subplot(313)
					plt.plot(o.errnotatklist)
					plt.title('Observer error prediction not attack (1=error)')
					plt.ylabel('Error not atk')
					plt.xlabel('t')
					plt.savefig(nameep + 'atkvarkepsilon' + str(epsilon*10))
					#plt.show()
					plt.close()
						

					
					del r
					del o
				f.close()
				env.destroye()
				del env.g
				del env



'''



