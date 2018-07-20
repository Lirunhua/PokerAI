from main import Main
#from thread import start_new_thread
import threading
import os.path

class Train(threading.Thread):
	def __init__(self, name, files):
		super().__init__()
		self.main = Main(name, files)

	def run(self):
		self.main.doListen()

# Create a new generation.
survivors = []
population = []
for i in range(160):
	files = ["../data/file1_%d.txt"%i,"../data/file2_%d.txt"%i,"../data/file3_%d.txt"%i]
	for f in files:
		if i not in survivors and os.path.exists(f):
			os.remove(f)
	population.append(Train('GLaDOS' + str(i), files))
	population[i].start()