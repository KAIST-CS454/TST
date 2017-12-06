import random

class Ant:
	def Ant(seq):
		self.currentPath = seq
		self.fitness = -1

	def traverse(graph, pheromone, seqLength):
		newSeq = []
		node = graph.start()
		for i in range(seqLength):
			newSeq.append(selectAction(node, graph, pheromone))
		self.currentPath = newSeq

	def calcFitness(g):
		self.fitness = fitness(self.currentPath, g)

class Graph:
	def Graph(n, matrix, startPoints):
		self.size = n 
		self.adjMatrix = matrix
		self.startPoints = startPoints

	def start():
		return(startPoints[random.randrange(len(startPoints))])

	def getRandomSeq(length):
		# random sequence generation

class Pheromone:
	def Pheromone(n, initP):
		self.adjMatrix = initP;
		self.size = n;

	def update(antSet):
		# pheromone update

def selectAction(node, g, p):
	# select next action after node
	# from g depending on p

def fitness(seq, g):
	# calculate fitness of sequence
	# related to g maybe?
	# 아마 논문읽고 필요한 argument 더 정해야할듯

def getBestSeq(antSet):
	# get best sequence via merging/selecting with ants

if __name__ == '__main__':
	antSize = 20
	generation = 1000
	seqLength = 50

	# n, matrix, initialNodes from 'known graph'
	g = Graph(n, matrix, initialNodes)
	p = Pheromone(n, initP)

	antList = range(antSize)
	for i in range(antSize):
		antList[i] = Ant(g.getRandomSeq(seqLength))
		antList[i].calcFitness(g)

	for i in range(generation):
		for j in range(antSize):
			antList[j].traverse(g, p, seqLength)
			antList.calcFitness(g)
		p.update(antList)

	bestSeq = getBestSeq(antList)

	# extract bestSeq as our known form


