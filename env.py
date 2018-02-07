class Node:
	def __init__(self,pos,cover=0):
		self.pos=pos
		self.cover=cover
		self.adj=[]

	def addadj(self,n):
		if n not in self.adj:
			self.adj.append(n)
			#n.adj.append(self) non necessaria
	
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


class Env:
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
		
	def printenv(self):
		for a in g.matnodes:
			x=g.getnode(a)
			print(x.pos, ":", end="")
			for n in x.adj:
				print(" ", n.pos,  end="")
				if n.cover:
					print('()', end="")
			print()


g=Env()
n1=Node('1')
n2=Node('2')
n3=Node('3')
n4=Node('4')
n5=Node('5')
n6=Node('6')
n7=Node('7')
n8=Node('8')
n9=Node('9')
n10=Node('10')
n11=Node('11')
n12=Node('12')
n13=Node('13')
n14=Node('14')

n8.setcover(1)
n9.setcover(1)
n10.setcover(1)

g.addnode(n1)
g.addnode(n2)
g.addnode(n3)
g.addnode(n4)
g.addnode(n5)
g.addnode(n6)
g.addnode(n7)
g.addnode(n8)
g.addnode(n9)
g.addnode(n10)
g.addnode(n11)
g.addnode(n12)
g.addnode(n13)
g.addnode(n14)



g.addedge(n1,n2)
g.addedge(n2,n3)
g.addedge(n2,n4)
g.addedge(n2,n5)
g.addedge(n2,n11)
g.addedge(n3,n4)
g.addedge(n3,n6)
g.addedge(n5,n8)
g.addedge(n7,n8)
g.addedge(n7,n9)
g.addedge(n8,n9)
g.addedge(n8,n10)
g.addedge(n9,n10)
g.addedge(n10,n14)
g.addedge(n10,n11)
g.addedge(n11,n12)
g.addedge(n11,n13)
g.addedge(n12,n14)
g.addedge(n12,n13)



g.printenv()
	
