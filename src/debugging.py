from main import Main
import threading

if __name__ == '__main__':
	thread = [threading.Thread(target=Main('GLaDOS%d'%i).doListen) for i in range(20)]

	for t in thread:
		t.start()

	for t in thread:
		t.join()
