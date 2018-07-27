from main import Main
import threading

if __name__ == '__main__':
  main = [Main('GLaDOS%d'%i) for i in range(10)]
  thread = []
  for m in main:
    m.debugMode = True
	  thread.append(threading.Thread(target=m.doListen))

	for t in thread:
		t.start()

	for t in thread:
		t.join()
