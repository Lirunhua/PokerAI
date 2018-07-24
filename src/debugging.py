from main import Main
import threading

if __name__ == '__main__':
    m1 = Main('GLaDOS')
    m2 = Main('GLaDOS2')
    m3 = Main('GLaDOS3')

    m1.debugMode = True
    m2.debugMode = True
    m3.debugMode = True

    t1 = threading.Thread(target=m1.doListen)
    t2 = threading.Thread(target=m2.doListen)
    t3 = threading.Thread(target=m3.doListen)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()