import socket
import threading
import sys
import pickle
import os

host = "localhost"
port = 4000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def proceso():
    sock.send(pickle.dumps(os.getpid()))
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    while True:
        pass

def main():
    sock.connect((str(host), int(port)))

    process = threading.Thread(target=proceso)

    process.daemon = True
    process.start()