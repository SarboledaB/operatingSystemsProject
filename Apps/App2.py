import socket
import threading
import sys
import pickle
import os

def App2Init():
    try:
        os.system('notepad')
        return True
    except:
        return False

def App2Stop(process):
    try:
        return True
    except:
        return False