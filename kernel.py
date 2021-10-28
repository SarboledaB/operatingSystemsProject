import socket
import threading
import sys
import pickle
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
            print(conn)
            modules['AppicationModule'] = conn
            print(modules)
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
            print(conn)
            modules['GUIModule'] = conn
            print(modules)
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
            print(conn)
            modules['FileManager'] = conn
            print(modules)
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
            except:
                pass

def processAPPCon():
    	while True:
            try:
                if modules['AppicationModule'] != '':
                    dataAPP = modules['AppicationModule'].recv(1024)
                    if dataAPP:
                        print(pickle.loads(dataAPP))
            except:
                pass
    
def processFILECon():
    	while True:
            try:
                if modules['FileManager'] != '':
                    dataFILE = modules['FileManager'].recv(1024)
                    if dataFILE:
                        print(pickle.loads(dataFILE))
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
    while True:
        msg = input('->')
        if msg == 'salir':
            sock.close()
            sys.exit()
        elif msg == 'send':
            if prueba['dst'] == 'APP':
                if modules['AppicationModule'] != '':
                    modules['AppicationModule'].send(pickle.dumps(prueba))
            elif prueba['dst'] == 'FILE':
                if modules['FileManager'] != '':
                    modules['FileManager'].send(pickle.dumps(prueba))