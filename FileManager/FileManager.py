import socket
import threading
import sys
import pickle
import os

class FileManager(object):

    def __init__(self, *args):
        super(FileManager, self).__init__(*args)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 4000))

        def fileProceso():
            while True:
                try:
                    data = sock.recv(1024)
                    if data:
                        data = pickle.loads(data)
                        print(data)
                        if data['cmd'] == 'create':
                            try:
                                os.mkdir(data['msg'])
                                sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                            except:
                                sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                        elif data['cmd'] == 'delete':
                            try:
                                os.rmdir(data['msg'])
                                sock.send(pickle.dumps({'codeterm': 0, 'msg': 'OK'}))
                            except:
                                sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))
                except:
                    sock.send(pickle.dumps({'codeterm': 2, 'msg': 'Err'}))

        processFile = threading.Thread(target=fileProceso)

        processFile.daemon = True
        processFile.start()