import socket
import threading
import sys
import pickle
import os
import psutil
import time

from Apps.App1 import App1Init, App1Stop
from Apps.App2 import App2Init, App2Stop

applications = {
    'APP1': '',
    'APP2': ''
}

class ApplicationModule(object):


    def __init__(self, *args):
        super(ApplicationModule, self).__init__(*args)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 4000))  

        
        def proceso():
            global applications
            while True:
                try:
                    data = sock.recv(1024)
                    if data:
                        data = pickle.loads(data)
                        if data['msg'] == 'APP1':
                            if data['cmd'] == 'close':
                                if applications['APP1'] != '': 
                                    if App1Stop():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                        applications['APP1'] = ''
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                            elif data['cmd'] == 'open':   
                                if applications['APP1'] == '': 
                                    if App1Init():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                        applications['APP1'] = 'ocupada'
                                        process_app1 = threading.Thread(target=ActiveApp1)
                                        process_app1.daemon = True
                                        process_app1.start()
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 1, 'msg': 'O'}))
                        elif data['msg'] == 'APP2':
                            if data['cmd'] == 'close':
                                if applications['APP2'] != '': 
                                    if App2Stop():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                        applications['APP2'] = ''
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                            elif data['cmd'] == 'open':   
                                if applications['APP2'] == '': 
                                    if App2Init():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                        applications['APP2'] = 'ocupada'
                                        process_app2 = threading.Thread(target=ActiveApp2)
                                        process_app2.daemon = True
                                        process_app2.start()
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 1, 'msg': 'O'}))
                        elif data['msg'] == 'APP':
                            if data['cmd'] == 'close':
                                if applications['APP1'] != '':
                                    applications['APP1'] = ''
                                    if App1Stop():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                if applications['APP2'] != '': 
                                    applications['APP2'] = ''
                                    if App2Stop():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                try:
                                    sock.close()
                                except print(0):
                                    sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                        else:
                            sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                except:
                    pass

        process = threading.Thread(target=proceso)

        process.daemon = True
        process.start()

        def ActiveApp1():
            global applications
            running = True
            while running:
                count = 0
                for p in psutil.process_iter():
                    if p.name() == 'Calculator.exe' or p.name() == 'CalculatorApp.exe':
                        count=1
                running = (count == 1)
            try:
                sock.send(pickle.dumps({'codeterm': 4, 'msg': 'APP1'}))
            except:
                pass
            applications['APP1'] = ''
            
        def ActiveApp2():
            global applications
            time.sleep(2)
            running = True
            while running:
                count = 0
                for p in psutil.process_iter():
                    if p.name() == 'mspaint.exe':
                        count=1
                running = (count == 1)
            try:
                sock.send(pickle.dumps({'codeterm': 4, 'msg': 'APP2'}))
            except:
                pass
            applications['APP2'] = ''
    
  



        


        