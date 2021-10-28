import socket
import threading
import sys
import pickle
import os
import subprocess
import time
import psutil

def App():
    try:
        os.system('mspaint')
        return True
    except:
        return False

def App2Init():
    processFile = threading.Thread(target=App)
    processFile.daemon = True
    processFile.start()
    return True

def App2Stop():
    try:
        for p in psutil.process_iter():
            if p.name() == 'mspaint.exe':
                os.system('taskkill /F /PID {0}'.format(p.pid))
        return True
    except:
        return False

 