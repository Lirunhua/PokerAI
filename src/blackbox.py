import random
import numpy

# create a recurring neural network with 
class BlackBox:
	def __init__(self, cardSize, playerSize, inputSize, outputSize):
		self.outputSize = outputSize
		self.network = self.Network('sigmoid', inputSize + 20, outputSize, 5)# dummy data
		self.handNetwork = self.Network('sigmoid', cardSize, 10, cardSize) # not final
		self.playerNetwork = self.Network('tanh', playerSize, 10, playerSize) # not final

	# constructor for training
	def clone(self, other):
		self.outputSize = other.outputSize
		self.network.clone(other.network)
		self.handNetwork.clone(other.handNetwork)
		self.playerNetwork.clone(other.playerNetwork)

	def newGame(self):
		self.handNetwork.resetRecursion()
		self.playerNetwork.resetRecursion()
		self.network.resetRecursion()


	def run(self, cards, playersData, otherData):
		if len(cards) == 2:
			self.handNetwork.resetRecursion()
		handOut = []
		for c in cards:
			handOut = self.handNetwork.run(c)

		playerOut = []
		for p in playersData:
			playerOut = self.playerNetwork.run(p)

		return self.network.run(otherData + handOut + playerOut)

	class Network:
		def __init__(self, functionType, inputSize, outputSize, recursionSize, layers = 1):
			self.functionType = functionType
			self.layers = layers if layers > 0 else 1
			self.inputSize = inputSize + recursionSize
			self.outputSize = outputSize + recursionSize
			self.layerSize = (self.inputSize + self.outputSize) * 2 // 3
			self.index = outputSize
			self.recursion = [0] * recursionSize
			self.interval = 8
			self.layerMatrix = []
			self.offset = []
			self.__createLayer__(self.inputSize, self.layerSize)
			for i in range(self.layers - 1):
				self.__createLayer__(self.layerSize, self.layerSize)
			self.__createLayer__(self.layerSize, self.outputSize)

		def __createLayer__(self, inputSize, outputSize):
			# TODO make this read a file.
			self.layerMatrix.append([[random.randrange(-self.interval, self.interval) for j in range(inputSize)] for i in range(outputSize)])
			self.offset.append([random.randrange(-self.interval, self.interval) for i in range(outputSize)])

		# Constructor useful for training
		def clone(self, other):
			self.functionType = other.functionType
			self.inputSize = other.inputSize
			self.outputSize = other.outputSize
			self.index = other.index
			self.recursion = other.recursion
			self.interval = other.interval
			self.layerMatrix = other.layerMatrix
			self.offset = other.offset
			# Allow multiple mutations
			for i in range(random.randint(0, layers + 2)):
				self.mutate()

		def resetRecursion(self):
			self.recursion = [0 for i in self.recursion]

		def run(self, inputData):
			inputData.extend(self.recursion)
			output = inputData + self.recursion
			for layer in range(len(self.layerMatrix)):
				output = [self.f(self.offset[layer][i] + sum([output[j] * self.layerMatrix[layer][i][j] 
					for j in range(len(self.layerMatrix[layer][i]))])) 
					for i in range(len(self.layerMatrix[layer]))]
			self.recursion = output[self.index:]
			return output[:self.index]

		# Mutates one value, usually by a small amount but can be a large amount.
		def mutate(self):
			r = random.randrange(-self.interval**4, self.interval**4)
			r = r if r==0 else self.interval / r
			l = random.randint(0, len(self.layerMatrix) - 1)
			o = random.randint(0, len(self.layerMatrix[l]) - 1)
			i = random.randint(0, len(self.layerMatrix[l][o]))
			
			if i == self.inputSize:
				self.offset[l][o] += r
			else:
				self.layerMatrix[l][o][i] += r


		# Selects the given function for this network, default is linear
		def f(self, x):
			y = x
			if self.functionType == 'sigmoid':
				y = 1/(1+numpy.exp(-x))
			elif self.functionType == 'tanh':
				y = numpy.tanh(x)
			return y
# Example
#b = BlackBox(3, 3, 3, 3)
#b.newGame
#print(b.run([[1,2,3],[3,4,2]], [[4,5,6],[1,3,5],[4,2,6]], [7,8,9]))
#b2 = BlackBox(3, 3, 3, 3).clone(b)