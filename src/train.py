import main
from thread import start_new_thread

class Train:
	def __init__(self, name):
		self.name = name

	def run(self):
		main.doListen(name)

# create a new generation
population = []
for i in range(160):
	population.append(Train('GLaDOS' + str(i)))
	start_new_thread(population[i].run)