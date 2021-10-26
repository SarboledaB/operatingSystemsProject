import socket
import threading
import sys
import pickle

host = "localhost"
port = 4000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    sock.connect((str(host), int(port)))
        

    