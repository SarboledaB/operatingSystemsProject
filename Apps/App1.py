import socket
import threading
import sys
import pickle
import os
import subprocess
import time
import psutil

def App1Init():
    try:
        os.system('calc')
        return True
    except:
        return False

def App1Stop():
    try:
        for p in psutil.process_iter():
            if p.name() == 'Calculator.exe' or p.name() == 'CalculatorApp.exe':
                print(p, p.name(), p.pid)
                os.system('taskkill /F /PID {0}'.format(p.pid))
                return True
        return True
    except:
        return False
 


    