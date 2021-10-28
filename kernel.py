import socket
import threading
import sys
import pickle
import datetime
from Apps.ApplicationModule import ApplicationModule
from FileManager.FileManager import FileManager
from GUI import main as GUI

host="localhost"
port=4000
modules = {
    "AppicationModule" : '',
    "FileManager"      : '',
    "GUIModule"        : '',
}

codes = {
    0: 'Procesado',
    1: 'Ocupado',
    2: 'Err',
    3: 'Procesado',
    4: 'Terminado'
}

prueba = {'cmd': 'delete', 'src': 'GUI', 'dst': 'FILE', 'msg': 'ARCHIVO1'}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((str(host), int(port)))
sock.listen(10)
sock.setblocking(False)

def acceptConAppicationModule():
    x = True
    while x:
        try:
            conn, addr = sock.accept()
            conn.setblocking(False)
            modules['AppicationModule'] = conn
            if modules['AppicationModule'] != '':
              x = False  
        except:
            pass

def acceptConGUIModule():
    x = True
    while x:
        try:
            conn, addr = sock.accept()
            conn.setblocking(False)
            modules['GUIModule'] = conn
            if modules['GUIModule'] != '':
              x = False  
        except:
            pass

def acceptConFileManager():
    x = True
    while x:
        try:
            conn, addr = sock.accept()
            conn.setblocking(False)
            modules['FileManager'] = conn
            if modules['FileManager'] != '':
              x = False  
        except:
            pass

def processGUICon():
    	while True:
            try:
                if modules['GUIModule'] != '':
                    dataGUI = modules['GUIModule'].recv(1024)
                    if dataGUI:
                        if pickle.loads(dataGUI)['dst'] == 'APP':  
                            modules['AppicationModule'].send(pickle.dumps(pickle.loads(dataGUI)))
                        elif pickle.loads(dataGUI)['dst'] == 'FILE':
                            modules['FileManager'].send(pickle.dumps(pickle.loads(dataGUI)))
                        msg = str(datetime.datetime.now()) + '->' + pickle.loads(dataGUI)['cmd'] + ' ' + pickle.loads(dataGUI)['msg']
                        log = {'cmd': 'send','src': 'GUI', 'dest': 'FILE', 'msg': msg}
                        modules['FileManager'].send(pickle.dumps(log))
            except:
                pass

def processAPPCon():
    	while True:
            try:
                if modules['AppicationModule'] != '':
                    dataAPP = modules['AppicationModule'].recv(1024)
                    if dataAPP:
                        if pickle.loads(dataAPP)['codeterm'] == 4:
                            msg = str(datetime.datetime.now()) + '->' + codes[pickle.loads(dataAPP)['codeterm']] + ' ' + pickle.loads(dataAPP)['msg']
                            log = {'cmd': 'send','src': 'APP', 'dest': 'FILE', 'msg': msg}
                            modules['FileManager'].send(pickle.dumps(log))
                        else:
                            msg = str(datetime.datetime.now()) + '->' + codes[pickle.loads(dataAPP)['codeterm']] + ' ' + 'APP'
                            log = {'cmd': 'send','src': 'APP', 'dest': 'FILE', 'msg': msg}
                            modules['FileManager'].send(pickle.dumps(log))
            except:
                pass
    
def processFILECon():
    	while True:
            try:
                if modules['FileManager'] != '':
                    dataFILE = modules['FileManager'].recv(1024)
                    if dataFILE:
                        if pickle.loads(dataFILE)['codeterm'] == 3:
                            msg = str(datetime.datetime.now()) + '->' + codes[pickle.loads(dataFILE)['codeterm']] + ' ' + 'FILE'
                            log = {'cmd': 'send','src': 'FILE', 'dest': 'GUI', 'msg': msg}
                            modules['FileManager'].send(pickle.dumps(log))
                            modules['GUIModule'].send(pickle.dumps(pickle.loads(dataFILE)))
                        else:
                            msg = str(datetime.datetime.now()) + '->' + codes[pickle.loads(dataFILE)['codeterm']] + ' ' + 'FILE'
                            log = {'cmd': 'send','src': 'FILE', 'dest': 'FILE', 'msg': msg}
                            modules['FileManager'].send(pickle.dumps(log))
            except:
                pass

def ApplicationModuleCon():
    accept = threading.Thread(target=acceptConAppicationModule)

    accept.daemon = True
    accept.start()

    process = threading.Thread(target=processAPPCon)

    process.daemon = True
    process.start()

    ApplicationModule()

def FileManagerCon():
    accept = threading.Thread(target=acceptConFileManager)

    accept.daemon = True
    accept.start()

    process = threading.Thread(target=processFILECon)

    process.daemon = True
    process.start()

    FileManager()

def GUICon():
    accept = threading.Thread(target=acceptConGUIModule)

    accept.daemon = True
    accept.start()

    process = threading.Thread(target=processGUICon)

    process.daemon = True
    process.start()

    GUI()

def initialization():
    FileManagerCon()
    ApplicationModuleCon()
    GUICon()

def execution():
    pass

def ending():
    pass


if __name__ == '__main__':
    initialization()