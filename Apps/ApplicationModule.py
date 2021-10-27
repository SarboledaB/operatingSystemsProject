import socket
import threading
import sys
import pickle
import os
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
                            if data['cmd'] == 'stop':
                                if applications['APP1'] != '': 
                                    if App1Stop(applications['APP1']):    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 1, 'msg': 'O'}))
                            elif data['cmd'] == 'open':   
                                if applications['APP1'] == '': 
                                    if App1Init():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                        applications['APP1'] = 'ocupada'
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 1, 'msg': 'O'}))
                        elif data['msg'] == 'APP2':
                            if data['cmd'] == 'stop':
                                if applications['APP2'] != '': 
                                    if App2Stop(applications['APP2']):    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 1, 'msg': 'O'}))
                            elif data['cmd'] == 'open':   
                                if applications['APP2'] == '': 
                                    if App2Init():    
                                        sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                                        applications['APP2'] = 'ocupada'
                                    else:
                                        sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                                else:
                                    sock.send(pickle.dumps({'codeterm': 1, 'msg': 'O'}))
                        else:
                            sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                except:
                    sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))

        process = threading.Thread(target=proceso)

        process.daemon = True
        process.start()



        


        