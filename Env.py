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


class Graph:
	def __init__(self,numnodes=0):
		self.numnodes=numnodes
		self.nodes=[]
		self.matnodes={}

	def getnode(self,n):
		return self.nodes[self.matnodes[n]]

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

	def listnode(self):
		return self.nodes[:]
		
	def printg(self):
		for a in self.matnodes:
			x=self.getnode(a)
			print(x.pos, ":", end="")
			for n in x.adj:
				print(" ", n.pos,  end="")
				if n.cover:
					print('()', end="")
			print()

class Environment:
	def __init__(self,n):
		aux=[]
		g=Graph()
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
					
		for x in range(randint(0,(len(g.nodes)*len(g.nodes)-1)/2)):			#aggiunta archi
			print(x)
			c=randint(0,len(g.nodes)-1)
			r=randint(0,len(g.nodes)-1)
			if c != r:
				g.addedge(g.nodes[c],g.nodes[r])
		
		
		g.printg()

e=Environment(7)
