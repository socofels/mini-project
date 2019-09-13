from threading import Thread, current_thread, active_count
from time import sleep
def down():
    while True:
        temp = input("输入Q关闭时钟")
        if temp == "q":
            exit()
def loop():
    while True:
        if thread1.is_alive():
            sleep(10)
        else:
            exit()


thread1 = Thread(target=down, name="down")
thread2 = Thread(target=loop, name="loop")

thread1.start()
thread2.start()

thread1.join()
thread2.join()
