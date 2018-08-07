import random
import numpy
import json
import sys, os.path

# create a recurring neural network with 
class BlackBox:
    def __init__(self, filenameArray, cardSize, playerSize, inputSize, outputSize):
        self.outputSize = outputSize
        self.filenameArray = filenameArray
        self.network = self.Network(filenameArray[0], 'sigmoid', inputSize + 20, outputSize, 5)# dummy data
        self.handNetwork = self.Network(filenameArray[1], 'sigmoid', cardSize, 10, cardSize) # not final
        self.playerNetwork = self.Network(filenameArray[2], 'tanh', playerSize, 10, playerSize) # not final

    # constructor for training
    def clone(self, other):
        self.outputSize = other.outputSize
        self.network.clone(other.network)
        self.handNetwork.clone(other.handNetwork)
        self.playerNetwork.clone(other.playerNetwork)

    def cross(self, other):
        self.network.cross(other.network)
        self.handNetwork.cross(other.handNetwork)
        self.playerNetwork.cross(other.playerNetwork)

    def newGame(self):
        self.handNetwork.resetRecursion()
        self.playerNetwork.resetRecursion()
        self.network.resetRecursion()

    def run(self, cards, playersData, otherData):
        if len(cards) == 2:
            self.handNetwork.resetRecursion()
        handOut = [0] * 10
        for c in cards:
            handOut = self.handNetwork.run(c)

        playerOut = [0] * 10
        for p in playersData:
            playerOut = self.playerNetwork.run(p)

        return self.network.run(otherData + handOut + playerOut)

    def saveAll(self):
        self.network.save(self.filenameArray[0])
        self.handNetwork.save(self.filenameArray[1])
        self.playerNetwork.save(self.filenameArray[2])

    class Network:
        def __init__(self, filename, functionType, inputSize, outputSize, recursionSize, layers = 1):
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
            self.load(filename)

        def __createLayer__(self, inputSize, outputSize):
            self.layerMatrix.append([[random.randrange(-self.interval, self.interval) for j in range(inputSize)] for i in range(outputSize)])
            self.offset.append([random.randrange(-self.interval, self.interval) for i in range(outputSize)])

        def save(self,filename):
            with open(filename, 'w+') as f:
                json.dump([self.offset, self.layerMatrix],f)
    
        def load(self,filename):
            if os.path.isfile(filename) :
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.layerMatrix = data[1]
                    self.offset = data[0]
                    # print("loaded from file %s",filename)
            else:
                self.__createLayer__(self.inputSize, self.layerSize)
                for i in range(self.layers - 1):
                    self.__createLayer__(self.layerSize, self.layerSize)
                self.__createLayer__(self.layerSize, self.outputSize)

        # Constructor useful for training
        def clone(self, other):
            self.layerMatrix = [[matrix[:] for matrix in layer] for layer in other.layerMatrix]
            self.offset = [o[:] for o in other.offset]

        def cross(self, other):
            try:
                for l in range(self.layers + 1):
                    for i in range(len(self.layerMatrix[l])):
                        if random.getrandbits(1):
                            self.layerMatrix[l][i] = other.layerMatrix[l][i][:]
                            self.offset[l][i] = other.offset[l][i]
                # Allow multiple mutations
                for i in range(random.randint(0, self.inputSize * (self.layers + 1))):
                    self.mutate()
            except Exception as e:
                print("Error during cross")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                sys.stdout.flush()

        def resetRecursion(self):
            self.recursion = [0 for i in self.recursion]

        def run(self, inputData):
            output = inputData[:] + self.recursion[:]
            for layer in range(len(self.layerMatrix)):
                output = [self.f(float(self.offset[layer][i]) + sum([float(output[j]) * float(self.layerMatrix[layer][i][j])
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
            
            if i == len(self.layerMatrix[l][o]):
                self.offset[l][o] += r
            else:
                self.layerMatrix[l][o][i] += r

        # Selects the given function for this network, default is linear
        def f(self, x):
            y = x
            if self.functionType == 'sigmoid':
                y = 1 / (1 + numpy.exp(-x))
            elif self.functionType == 'tanh':
                y = numpy.tanh(x)
            return y


# Testing
if __name__ == '__main__':
    filenameArray = ["../data/file1.txt","../data/file2.txt","../data/file3.txt"]
    b = BlackBox(filenameArray, 6, 7, 7, 6)
    b.newGame
    b.saveAll()
    b2 = BlackBox(filenameArray,6, 7, 7, 6).clone(b)
