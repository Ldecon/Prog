from random import random, randint


class Node:
	def __init__(self,pos,imp=0,cover=0):
		self.pos=pos
		self.cover=cover
		self.adj=[]
		self.imp=imp
		self.cont=0
		self.lastvisit=0
		self.valueimp=0

	def addadj(self,n):
		if n not in self.adj:
			self.adj.append(n)
	
	def remadj(self,n):
		if n in self.adj:
			self.adj.remove(n)
	
	def setcover(self,c):
		self.cover=c
	
	def listadj(self):		
		return self.adj[:]

	def __eq__(self,n):
		return n.pos==self.pos

	def __ne__(self,n):
		return not(n==self)
	
	def __hash__(self):
        	return self.pos.__hash__()


class Edge:
	def __init__(self,n1,n2,w=0):
		self.n1=n1
		self.n2=n2
		self.w=w
	

class Graph:
	def __init__(self,numnodes=0):
		self.numnodes=numnodes
		self.nodes=[]
		self.edges=[]
		self.matnodes={}
		
	def getnode(self,n):
		return self.nodes[self.matnodes[n]]
		
	def getweightedge(self,n1,n2):
		for x in range(len(self.edges)):
				if ((self.edges[x].n1.pos == n1.pos) and (self.edges[x].n2.pos == n2.pos))or((self.edges[x].n1.pos == n2.pos) and (self.edges[x].n2.pos == n1.pos)):
					return self.edges[x].w
		return 0

	def existedge(self,n1,n2):
		for x in range(len(self.edges)):
			if ((self.edges[x].n1.pos == n1.pos) and (self.edges[x].n2.pos == n2.pos))or((self.edges[x].n1.pos == n2.pos) and (self.edges[x].n2.pos == n1.pos)):
				return 1
		return 0
		
	def getedge(self,n1,n2):
		for x in range(len(self.edges)):
				if ((self.edges[x].n1.pos == n1.pos) and (self.edges[x].n2.pos == n2.pos))or((self.edges[x].n1.pos == n2.pos) and (self.edges[x].n2.pos == n1.pos)):
					return self.edges[x]
		return None		
							
	def addnode(self,n):
		if n not in self.matnodes:
			self.nodes.append(n)
			self.matnodes[n]=len(self.nodes)-1
			self.numnodes=self.numnodes+1
		return self.getnode(n)

	def addedge(self,n,m):
		n1= self.getnode(n)
		m1=self.getnode(m)
		n1.addadj(self.getnode(m))
		m1.addadj(self.getnode(n))
		if not self.existedge(n,m):
			e=Edge(n,m)
			self.edges.append(e)	
			
	def remedge(self,e):
		n1=self.getnode(e.n1)
		n2=self.getnode(e.n2)
		n1.remadj(self.getnode(e.n2))
		n2.remadj(self.getnode(e.n1))
		if self.existedge(n1,n2):
			self.edges.remove(self.getedge(self.getnode(n1),self.getnode(n2)))
				
	
	def setweightedge(self,n1,n2,w):
		for x in range(len(self.edges)):
			if ((self.edges[x].n1.pos == n1.pos) and (self.edges[x].n2.pos == n2.pos))or((self.edges[x].n1.pos == n2.pos) and (self.edges[x].n2.pos == n1.pos)):
				self.edges[x].w=w
			
	def trianglepath(self,n1,n2):					#scopre se c'è un percorso triangolare
		t=[]
		for x in range(len(n1.adj)):
			for y in range(len(n2.adj)):
				if (n1.adj[x].pos==n2.adj[y].pos)and(n1.adj[x] not in t):
					t.append(n1.adj[x])
		return t
			
	
	def printedges(self):
		for x in range(len(self.edges)):
			print('[',self.edges[x].n1.pos,',',self.edges[x].n2.pos,', w=',self.edges[x].w,']')
			
		
	def printg(self):
		for a in self.matnodes:
			x=self.getnode(a)
			print(x.pos, 'i=', x.imp, ":", end="")
			for n in x.adj:
				print(" ", n.pos,  end="")
				if n.cover:
					print('()', end="")
			print()
			
	def printgfile(self):
		f=open("Graph.txt","w")
		for a in self.matnodes:
			x=self.getnode(a)
			f.write(x.pos)
			f.write(' i=')
			f.write(str(x.imp))
			f.write(':')
			for n in x.adj:
				f.write(' ')
				f.write(n.pos)
				if n.cover:
					f.write('()')
			f.write('\n')
		for x in range(len(self.edges)):
			f.write('[')
			f.write(str(self.edges[x].n1.pos))
			f.write(',')
			f.write(str(self.edges[x].n2.pos))
			f.write(', w=')
			f.write(str(self.edges[x].w))
			f.write(']\n')
			
		f.close()	



class Environment:
	def __init__(self,n=0,file=0,g=Graph()):
		self.g=g
		self.n=n
		aux=[]
		self.file=file
		if not file:
			for x in range(n):
				aux.append(Node(str(x+1),imp=randint(1,20)))  #popolamento lista ausiliaria
			c=randint(0,n-1)
			self.g.addnode(aux[c])
			aux.pop(c)
			while aux:							#popolamento lista nodi grafo e svuotamento lista ausiliaria
				r=randint(0,len(self.g.nodes)-1)
				c=randint(0, len(aux)-1)
				self.g.addnode(aux[c])
				ndaux=self.g.getnode(aux[c])
				self.g.addedge(self.g.nodes[r],ndaux)
				w=randint(1,10)						#pesi possibili degli archi
				self.g.setweightedge(self.g.nodes[r],ndaux,w)      #all'arco attuale viene dato il peso w
				aux.pop(c)
			
			r=randint(0,int((len(self.g.nodes)*len(self.g.nodes)-1)/2))
			re=[]	
			for x in range(r):						#aggiunta un numero di archi casuale tra 0 e n(n-1)/2
				c=randint(0,len(self.g.nodes)-1)
				r=randint(0,len(self.g.nodes)-1)
				if (c != r) and(not self.g.existedge(self.g.nodes[c],self.g.nodes[r])):
					self.g.addedge(self.g.nodes[c],self.g.nodes[r])
					e=self.g.edges[len(self.g.edges)-1]
					t=self.g.trianglepath(e.n1,e.n2)
					if t:
						listab=[]
						lists=[]
						for y in range(len(t)):
							e1=self.g.getedge(e.n1,t[y])
							e2=self.g.getedge(t[y],e.n2)
							s=e1.w+e2.w
							ab=abs(e1.w-e2.w)
							listab.append(ab)
							listab.sort()
							lists.append(s)
							lists.sort()
							#print(e.n1.pos,'-',e.n2.pos,'#############################',e1.n1.pos,'-',e1.n2.pos,'(',e1.w,')','->',e2.n1.pos,'-',e2.n2.pos,'(',e2.w,')',s)	
						if (lists[0] >= listab[0])and(listab[len(listab)-1]<=lists[0]):
							if listab[len(listab)-1]==0:
								listab[len(listab)-1]=1
							ranw=randint(listab[len(listab)-1],lists[0])
							e.w=ranw
						else:
							re.append(e)	
					else:
						ranw=randint(1,10)
						e.w=ranw
						
				for y in range(len(re)):
					self.g.remedge(self.g.getedge(re[y].n1,re[y].n2))
				re=[]
							
			
		else:
			self.file=open('Graph.txt')
			r=self.file.readline()
			while r[0]!='[':					#da file inserimento nodi
				i=0
				s=''
				while r[i]!=' ':
					s=s+r[i]
					i=i+1
				n=Node(s)
				self.g.addnode(n)
				s=''
				while r[i]!='=':
					i=i+1
				i=i+1
				while r[i]!=':':
					s=s+r[i]
					i=i+1
				n.imp=int(s)
				r=self.file.readline()
					
			while r!='':					#da file inserimento archi
				i=1	
				s=''
				while r[i]!=',':
					s=s+r[i]
					i=i+1
				s1=''
				i=i+1
				while r[i]!=',':
					s1=s1+r[i]
					i=i+1
				n1=Node(s)
				n2=Node(s1)
				for x in range(len(self.g.nodes)):
					if n1.pos == self.g.nodes[x].pos:
						n1=self.g.getnode(self.g.nodes[x])
						break
				for x in range(len(self.g.nodes)):	
					if n2.pos == self.g.nodes[x].pos:
						n2=self.g.getnode(self.g.nodes[x])
						break
				self.g.addedge(n1,n2)
				e=self.g.getedge(n1,n2)
				while r[i]!='=':
					i=i+1
				i=i+1
				sw=''
				while r[i]!=']':
					sw=sw+r[i]
					i=i+1
				e.w=int(sw)
				r=self.file.readline()
			
			
		#self.g.printg()
		#self.g.printgfile()
		#self.g.printedges()
		
#e=Environment(10)				#creazione grafo da numero di nodi
#e=Environment(file=1)			#lettura grafo da file
