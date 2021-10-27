import socket
import threading
import sys
import pickle
import os

def App1Init():
    try:
        os.system('calc')
        return True
    except:
        return False

def App1Stop(process):
    try:
        return True
    except:
        return False
        


    