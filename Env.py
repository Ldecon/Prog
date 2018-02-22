from random import random, randint


class Node:
	def __init__(self,pos,cover=0):
		self.pos=pos
		self.cover=cover
		self.adj=[]

	def addadj(self,n):
		if n not in self.adj:
			self.adj.append(n)
	
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
	
	def setweight(self,w):
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
		for x in len(edges):
			if (self.edges[x].n1.pos == n1.pos) and (self.edges[x].n2.pos == n2.pos):
				return self.edges[x].w
		return 0

	def existedge(self,n1,n2):
		for x in range(len(self.edges)):
			if ((self.edges[x].n1.pos == n1.pos) and (self.edges[x].n2.pos == n2.pos))or((self.edges[x].n1.pos == n2.pos) and (self.edges[x].n2.pos == n1.pos)):
				return 1
		return 0
					
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

	def listnode(self):
		return self.nodes[:]
		
	def printedges(self):
		for x in range(len(self.edges)):
			print('[',self.edges[x].n1.pos,',',self.edges[x].n2.pos,', w=',self.edges[x].w,']')
			
		
	def printg(self):
		for a in self.matnodes:
			x=self.getnode(a)
			print(x.pos, ":", end="")
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
	def __init__(self,n=0,file=0):
		self.n=n
		aux=[]
		self.file=file
		g=Graph()
		if not file:
			for x in range(n):
				aux.append(Node(str(x+1)))  #popolamento lista ausiliaria
			c=randint(0,n-1)
			g.addnode(aux[c])
			aux.pop(c)
			while aux:							#popolamento lista nodi grafo e lista ausiliaria svuotata
				r=randint(0,len(g.nodes)-1)
				c=randint(0, len(aux)-1)
				g.addnode(aux[c])
				ndaux=g.getnode(aux[c])
				g.addedge(g.nodes[r],ndaux)
				aux.pop(c)
					
			r=randint(0,int((len(g.nodes)*len(g.nodes)-1)/2))	
			for x in range(r):	
				c=randint(0,len(g.nodes)-1)
				r=randint(0,len(g.nodes)-1)
				if c != r:
					g.addedge(g.nodes[c],g.nodes[r])
			
		else:
			self.file=open('Graph.txt')
			r=self.file.readline()
			while r[0]!='[':					#da file inserimento nodi
				i=0
				s=''
				while r[i]!=':':
					s=s+r[i]
					i=i+1
				n=Node(s)
				g.addnode(n)
				r=self.file.readline()
			print(r)
			
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
				for x in range(len(g.nodes)):
					if n1.pos == g.nodes[x].pos:
						n1=g.getnode(g.nodes[x])
						break
				for x in range(len(g.nodes)):	
					if n2.pos == g.nodes[x].pos:
						n2=g.getnode(g.nodes[x])
						break
				g.addedge(n1,n2)
				r=self.file.readline()
			
			
		g.printg()
		g.printedges()
		
e=Environment(7)					#creazione grafo da numero di nodi
#e=Environment(file=1)			#lettura grafo da file

