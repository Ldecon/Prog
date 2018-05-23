from random import random, randint
import math

class Node:
	def __init__(self,pos,imp=-1):
		self.pos=pos
		self.cx=-1
		self.cy=-1
		self.adj=[]
		self.imp=imp
		self.visitcount=0
		self.passcount=0
		self.lastvisit=0
		self.valueimp=0
		self.nidlavg=0

	def addadj(self,n):
		if n not in self.adj:
			self.adj.append(n)
	
	def remadj(self,n):
		if n in self.adj:
			self.adj.remove(n)
		
	def listadj(self):		
		return self.adj[:]
		
	def __del__(self):
		del self 	


class Edge:
	def __init__(self,n1,n2):
		self.n1=n1
		self.n2=n2
		self.w=math.sqrt(((n1.cx-n2.cx)**2)+((n1.cy-n2.cy)**2))	
		
class Graph:
	def __init__(self,numnodes=0, planex=100, planey=100):   		#plane=grandezza piano cartesiano default 100x100
		self.numnodes=numnodes
		self.nodes=[]
		self.edges=[]
		self.matnodes={}
		self.planex=planex
		self.planey=planey
		self.dispcoord=[]
		for i in range(self.planex):
			for j in range(self.planey):
				self.dispcoord.append([i,j])
		
	def getnode(self,n):
		for i in range(len(self.nodes)):
			if n.pos==self.nodes[i].pos :
				return self.nodes[i]
		return None
	
	def getedge(self,n1,n2):
		for x in range(len(self.edges)):
				if ((self.edges[x].n1.pos == n1.pos) and (self.edges[x].n2.pos == n2.pos))or((self.edges[x].n1.pos == n2.pos) and (self.edges[x].n2.pos == n1.pos)):
					return self.edges[x]
		return None
	
	
	def getweightedge(self,n1,n2):
		e=self.getedge(n1,n2)
		if e:
			return self.edges[x].w
		return 0
			
			
	def existedge(self,n1,n2):
		e=self.getedge(n1,n2)
		if e:
			return 1
		return 0	
			
	def addnode(self,n):
		if n not in self.matnodes:
			r=randint(0,len(self.dispcoord)-1)
			n.cx=self.dispcoord[r][0]
			n.cy=self.dispcoord[r][1]
			self.dispcoord.pop(r)
			self.nodes.append(n)
			self.matnodes[n]=len(self.nodes)-1
			self.numnodes=self.numnodes+1
		return 
	
	def remnode(self,n):
		self.nodes.remove(n)
		self.numnodes=self.numnodes-1
		return
	
	def addedge(self,n,m):
		n1= self.getnode(n)
		m1=self.getnode(m)
		n1.addadj(self.getnode(m))
		m1.addadj(self.getnode(n))
		if not self.existedge(n,m):
			e=Edge(n,m)
			self.edges.append(e)	
		return
			
	def remedge(self,e):
		n1=self.getnode(e.n1)
		n2=self.getnode(e.n2)
		n1.remadj(self.getnode(e.n2))
		n2.remadj(self.getnode(e.n1))
		if self.existedge(n1,n2):
			self.edges.remove(self.getedge(self.getnode(n1),self.getnode(n2)))
		return
		
	def setimpn(self,n,i):
		n.imp=i
		return
	
	def critnodes(self,ln,num):			#scelta nodi critici
		lc=[]
		if len(ln[0].adj) < (len(ln)-2):
				lc.append(ln[0])
		for x in range(len(ln)):
			if ln[x] not in lc:
				flag=0
				for y in range(len(lc)):
					if ln[x] in lc[y].adj:
						flag=1
				if not flag:
					lc.append(ln[x])
		d=len(lc)-num
		if d == -num:						#se ogni nodo è collegato con ognuno
			lc.append(ln[randint(0,len(ln)-1)])
		else:
			while d > 0:				#se la lista dei possibili nodi critici ha più di num elementi, elimina casualmente la differenza di nodi, se ne ha meno tiene quelli che ha
				lc.pop(randint(0,len(lc)-1))
				d=d-1
		return lc
		
	def cascadeimp(self,n,i):			#nodo, importanza corrente  
		imp=i/2
		if (n.imp != -1)and(n.imp > imp):
			return
		else:
			self.setimpn(n,imp)
			for x in range(len(n.adj)):
				self.cascadeimp(n.adj[x],imp)
	
						
	def setimpg(self):		#setta importanza nodi grafo
		k=int(len(self.nodes)*0.2)				#percentuale di nodi critici
		lc=self.critnodes(self.nodes,k)
		for x in range(len(lc)):
			self.setimpn(lc[x],4)			#setta importanza nodi critici a 4
			for y in range(len(lc[x].adj)):
				self.cascadeimp(lc[x].adj[y],lc[x].imp)        #altro csacade aggiungere ,4
		
	
	def printedges(self):
		for x in range(len(self.edges)):
			print('[',self.edges[x].n1.pos,',',self.edges[x].n2.pos,', w=',self.edges[x].w,']')
			
		
	def printg(self):
		if len(self.nodes)==0:
			print("empty graph")
			return
		for a in self.matnodes:
			x=self.getnode(a)
			print(x.pos, ", coord=(",x.cx,",",x.cy,") i=", x.imp, ":", end="")
			for n in x.adj:
				print(" ", n.pos,  end="")
			print()
			
	def printgfile(self):
		f=open("Graph.txt","w")
		for a in self.matnodes:
			x=self.getnode(a)
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
		for x in range(len(self.edges)):
			f.write('[')
			f.write(str(self.edges[x].n1.pos))
			f.write(',')
			f.write(str(self.edges[x].n2.pos))
			f.write(', w=')
			f.write(str(self.edges[x].w))
			f.write(']\n')
			
		f.close()	

	def destroyg(self):
		while len(self.edges) :
			self.remedge(self.edges[0])
		while len(self.nodes) :
			del self.matnodes[self.nodes[0]]
			self.remnode(self.nodes[0])
		
			
	def __del__(self):
		del self	
			

class Environment:
	def __init__(self,n=0,file=0,g=Graph(),ed=-1):                          #n=numero nodi, file=no/sì caricamento da file, g=grafo,ed=coefficiente percentuale archi
		self.g=g
		self.n=n
		self.ed=ed
		self.file=file
		if not file:
			for x in range(n):
				g.addnode(Node(str(x+1)))				#inserimento nodi nell'ambiente
				for i in range(len(g.nodes)-1):
					g.addedge(g.nodes[len(g.nodes)-1],g.nodes[i])
			if self.ed<0 :
				ran=randint(0,((self.g.numnodes*(self.g.numnodes-1))/2)-(self.g.numnodes-1))      #numero casuale archi da 0 a (n*n-1/2)-n-1 (per preservare la componenete connessa)
			else:
				ran=int((((self.g.numnodes*(self.g.numnodes-1))/2)-(self.g.numnodes-1)) * (1-self.ed))      #si tolgono gli archi in percentuale dato da ed
			
			aux=[]
			edgetree=[]
			edgeposs=[]
			ln=g.nodes.copy()
			r1=randint(0,len(ln)-1)
			aux.append(ln[r1])
			ln.pop(r1)
			while ln:									#crea sottoalbero di connessioni
				ss=[]
				for i in range(len(aux)):
					if len(aux)==1:
						r1=1
					else:	
						r1=randint(0,len(ln)-1)	
					for j in range(r1):
						r2=randint(0,len(ln)-1)
						ss.append(ln[r2])
						edgetree.append(g.getedge(aux[i],ln[r2]))
						ln.pop(r2)
				if len(ln)==1:
					edgetree.append(g.getedge(edgetree[len(edgetree)-1].n1,ln[0]))
					ln.pop(0)
				aux=ss.copy()
			edgeposs=[i for i in g.edges if i not in edgetree]
			
			
			for i in range(ran):							#eliminazione archi
				r1=randint(0,len(edgeposs)-1)
				g.remedge(edgeposs[r1])
				edgeposs.pop(r1)
				
			self.g.setimpg()
		
		else:
			self.file=open('Graph.txt')
			r=self.file.readline()
			while r[0]!='[':					#da file inserimento nodi
				i=0
				s=''
				while r[i]!=',':
					s=s+r[i]
					i=i+1
				n=Node(s)
				self.g.addnode(n)
				s=''
				while r[i]!='(':
					i=i+1
				i=i+1
				while r[i]!=',':
					s=s+r[i]
					i=i+1
				n.cx=int(s)
				i=i+1
				s=''	
				while r[i]!=')':
					s=s+r[i]
					i=i+1
				n.cy=int(s)
				s=''	
				while r[i]!='=':
					i=i+1
				i=i+1
				while r[i]!=':':
					s=s+r[i]
					i=i+1
				n.imp=float(s)
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
				print(self.g.getnode(n1).pos,',',self.g.getnode(n2).pos)
				self.g.addedge(self.g.getnode(n1),self.g.getnode(n2))

				r=self.file.readline()
		
	def destroye(self):
		self.g.destroyg()
		del self	

				
	def __del__(self):
		del self
			
			
