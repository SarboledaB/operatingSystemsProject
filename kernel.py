import socket
import threading
import sys
import pickle
from Apps.App1 import main as app1

host="localhost"
port=4000

modules = []

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
            print(modules)
        except:
            pass


def initialization():
    app1()

def execution():
    pass

def ending():
    pass


if __name__ == '__main__':
    accept = threading.Thread(target=acceptCon)

    accept.daemon = True
    accept.start()
    initialization()
    while True:
        msg = input('->')
        if msg == 'salir':
            sock.close()
            sys.exit()
    