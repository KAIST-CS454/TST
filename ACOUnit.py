import random
from parseXML import XMLParser

# Ant class
class Ant:
	def __init__(self, seq):
		self.currentPath = seq
		self.fitness = -1

	# Ant traverse along graph, and pheromone value
	def traverse(self, graph, pheromone, seqLength, rho):
		newSeq = []
		node = graph.start()# randomly pick among initial points
		for i in range(seqLength):
			newSeq.append(selectAction(node, graph, pheromone, rho))
			# select action that can be reached from node
			# 0.7-pseudo random proportional rule
		self.currentPath = newSeq

	# Fitness calculation of current ant
	def calcFitness(self, g):
		self.fitness = fitness(self.currentPath, g)

# Graph class
class Graph:
	def __init__(self, n, matrix, startPoints):
		self.size = n 
		self.adjMatrix = matrix
		self.startPoints = startPoints

	# Randomly get among initial points
	def start(self):
		return(random.choice(ableIdx(self.startPoints)))

	# for ant initialization, get possible random sequence
	def getRandomSeq(self, length):
		seq = [self.start()]# random start point
		for j in range(length - 1):
			i = seq[j]
			ables = ableIdx(self.adjMatrix[i])# nodes that is able to be reached
			seq.append(random.choice(ables))# randomly choose among them
		return seq

# rho-based pseudo random propotional rule
def selectAction(node, g, p, rho):
	pheInfo = []
	ables = ableIdx(g.adjMatrix[node])
	phes = p.adjMatrix[node]
	for i in ables:
		pheInfo.append([i, phes[i]])# pheInfo is list of [nextIndex, pheromoneValue]
	
	def keyFun(t):# sorting key function
		return -t[1]# negation of pheromoneValue

	pheInfo.sort(key = keyFun)# sort pheInfo according to keyFunction

	if random.random() <= rho:# if in possibility rho
		return pheInfo[0][0]# get most-pheromoned index
	else:
		return random.choice(ables)# get random index

# fitness function of seq
def fitness(seq, g):
	isVisit = [False] * g.size# node visit flag
	fit = 0
	for s in seq:
		ables = ableIdx(g.adjMatrix[s])
		for i in ables:
			if not isVisit[i]:# if connected index was not counted
				fit += 1# add 1 to fitness value
				isVisit[i] = True# and switch flag as 'visited'
	return fit

# index list which are able to be reached.
# i.e. has value 1 in arr
def ableIdx(arr):
	indices = []
	for i in range(len(arr)):
		if arr[i] != 0:
			indices.append(i)
	return indices

# Pheromone class
class Pheromone:
	def __init__(self, n, initP, alpha):
		self.adjMatrix = [[initP] * n] * n# pheromones are initialized with initP value
		self.size = n;
		self.alpha = alpha# evaporation rate

	def update(self, antSet):
		newPhes = [[[0, 0]]*self.size] * self.size
		# list of list of [fitness sum, number of seq]
		# new pheromone values to be added

		# pheromone is related to edge(i, j)
		for ant in antSet:
			seq = ant.currentPath
			for i in range(len(seq) - 1):
				# i = seq[i], j = seq[j]
				# i.e. edge(i, j) is contained in ant's travel sequence
				newPhes[seq[i]][seq[i+1]][0] += ant.fitness# fitness addition
				newPhes[seq[i]][seq[i+1]][1] += 1# number of related sequence

		for i in range(self.size):
			for j in range(self.size):
				newPhe = 0
				if newPhes[i][j][1] > 0:# if edge(i, j) was related to ants
					newPhe = newPhes[i][j][0] / newPhes[i][j][1]
					# added pheromone is 'average of fitnesses'
				self.adjMatrix[i][j] = (1 - self.alpha) * self.adjMatrix[i][j] + self.alpha * newPhe
				# pheromone is also evaporated
				# and added with the new value
		return

# Select ant's sequence whose fitness is best
def getBestSeq(antSet):
	bestVal = -1
	bestSeq = []
	for ant in antSet:
		if ant.fitness > bestVal:
			bestSeq = ant.currentPath
			bestVal = ant.fitness
	return bestSeq, bestVal

def ACORun(antSize, generation, seqLength, initP, rho, alpha, EFGfile):
	parser = XMLParser(EFGfile)

	event_graph = parser.parse_event_graph()
	initial = parser.parse_event_initial()

	n = len(event_graph)
	g = Graph(n, event_graph, initial)
	p = Pheromone(n, initP, alpha)# initial pheromone value is 10

	# ant initialization
	antList = [None] * antSize
	for i in range(antSize):
		antList[i] = Ant(g.getRandomSeq(seqLength))
		antList[i].calcFitness(g)

	for i in range(generation):
		print("Generation:", i+1, "start")

		for j in range(antSize):
			antList[j].traverse(g, p, seqLength, rho)
			antList[j].calcFitness(g)
			
		p.update(antList)

	return getBestSeq(antList)
