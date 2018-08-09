from main import Main
import threading

if __name__ == '__main__':
    main = [Main('GLaDOS%d' % i, True) for i in range(5)]
    thread = []
    for m in main:
        m.debugMode = True
        thread.append(threading.Thread(target=m.doListen))

    for t in thread:
        t.start()

    for t in thread:
        t.join()