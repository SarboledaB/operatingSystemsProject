import socket
import threading
import sys
import pickle
from Apps.App1 import main as app1
from Apps.App2 import main as app2

host="localhost"
port=4000

modules = []
module = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((str(host), int(port)))
sock.listen(10)
sock.setblocking(False)

def acceptCon():
    while True:
        try:
            conn, addr = sock.accept()
            conn.setblocking(False)
            modules.append(conn)
        except:
            pass

def processCon():
    while True:
        if len(modules) > 0:
            for c in modules:
                try:
                    data = c.recv(1024)
                    if data:
                        module[pickle.loads(data)] = c
                except:
                    pass


def initialization():
    app1()
    app2()

def execution():
    pass

def ending():
    pass


if __name__ == '__main__':
    accept = threading.Thread(target=acceptCon)
    process = threading.Thread(target=processCon)

    accept.daemon = True
    accept.start()

    process.daemon = True
    process.start()
    initialization()
    while True:
        msg = input('->')
        if msg == 'salir':
            sock.close()
            sys.exit()
    