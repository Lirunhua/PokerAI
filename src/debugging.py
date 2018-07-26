from main import Main
import threading

if __name__ == '__main__':
	thread = [threading.Thread(target=Main('GLaDOS%d'%i).doListen) for i in range(10)]
	
	for t in thread:
		t.start()

	for t in thread:
		t.join()
