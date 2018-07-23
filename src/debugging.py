from main import Main
import threading

if __name__ == '__main__':
    m1 = Main('GLaDOS')
    t1 = threading.Thread(target=m1.doListen)
    t1.start()
    m2 = Main('GLaDOS2')
    t2 = threading.Thread(target=m2.doListen)
    t2.start()
    m3 = Main('GLaDOS3')
    t3 = threading.Thread(target=m3.doListen)
    t3.start()
    t1.join()
    t2.join()
    t3.join()