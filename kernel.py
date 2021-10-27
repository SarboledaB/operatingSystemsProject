import socket
import threading
import sys
import pickle
from Apps.ApplicationModule import ApplicationModule
from FileManager.FileManager import FileManager

host="localhost"
port=4000
modules = {
    "AppicationModule" : '',
    "FileManager" : ''
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

def processCon():
    	while True:
            try:
                if modules['AppicationModule'] != '':
                    data = modules['AppicationModule'].recv(1024)
                    if data:
                        print(pickle.loads(data)['msg'])
                if modules['FileManager'] != '':
                    data = modules['FileManager'].recv(1024)
                    if data:
                        print(pickle.loads(data)['msg'])
            except:
                pass

def ApplicationModuleCon():
    accept = threading.Thread(target=acceptConAppicationModule)

    accept.daemon = True
    accept.start()

    ApplicationModule()

def FileManagerCon():
    accept = threading.Thread(target=acceptConFileManager)

    accept.daemon = True
    accept.start()

    FileManager()

def initialization():
    FileManagerCon()
    ApplicationModuleCon()

def execution():
    pass

def ending():
    pass


if __name__ == '__main__':
    process = threading.Thread(target=processCon)

    process.daemon = True
    process.start()

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