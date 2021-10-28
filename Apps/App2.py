import socket
import threading
import sys
import pickle
import os
import psutil

def App2Init():
    try:
        os.system('notepad')
        return True
    except:
        return False

def App2Stop():
    try:
        for p in psutil.process_iter():
            if p.name() == 'notepad.exe':
                print(p, p.name(), p.pid)
                os.system('taskkill /F /PID {0}'.format(p.pid))
                return True
        return True
    except:
        return False
    
App2Init()
App2Stop()