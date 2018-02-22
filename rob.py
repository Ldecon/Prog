from env import Node, Edge, Graph, Environment
from random import randint


class Robot:
	def __init__(self,startpos):
		self.actualpos=startpos
		self.possiblepos=self.actualpos.adj
	
	def newactualpos(self,p):
		self.actualpos=p
		self.possiblepos=self.actualpos.adj

	def randomnextstep(self):
		p=self.possiblepos[randint(0,len(self.possiblepos)-1)]
		self.newactualpos(p)
		
	def printpossiblepos(self):
		print('possibles steps:', end=' ')
		for x in range(len(self.possiblepos)):
			print(self.possiblepos[x].pos,end=' ')
		print(end='\n')
		
	def randomsteps(self,ns):
		for x in range(ns):
			print('step ',x+1)
			print('robot in:',self.actualpos.pos)
			self.printpossiblepos()
			self.randomnextstep()
			

env=Environment(file=1)
n=env.g.nodes[randint(0,len(env.g.nodes)-1)]
r=Robot(n)
r.randomsteps(5)
