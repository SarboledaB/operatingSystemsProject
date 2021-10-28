import time
import threading
import logging
import socket
import threading
import sys
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    import tkinter as tk # Python 3.x
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText

class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

class myGUI(tk.Frame):

    def __init__(self, parent, window, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        if window == 'main':
            self.build_gui()
        elif window == 'apps':
            self.build_app()
        elif window == 'file_manager':
            self.build_file_manager()
    
    def build_file_manager(self):
        self.root.title('FILE MANAGER')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')

        entry = tk.Entry(self.root)
        entry.grid(row=1, column=0, sticky="nsew")
            
        button = tk.Button(self, text="Crear", command=lambda: send_message('create', 'FILE', entry.get()))
        button.configure(font='TkFixedFont')
        button.grid(row=2, column=1, sticky="nsew")

        button2 = tk.Button(self, text="Eliminar", command=lambda: send_message('delete', 'FILE', entry.get()))
        button2.configure(font='TkFixedFont')
        button2.grid(row=2, column=2, sticky="nsew")


    def build_app(self):
        self.root.title('APPS')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')

        label = tk.Label(self, text="Modulo de aplicaciones")
        label.configure(font='TkFixedFont')
        label.grid(row=0, column=0, sticky="w")

        button = tk.Button(self, text="Iniciar", command=lambda: send_message('open', 'APP','APP'))
        button.configure(font='TkFixedFont')
        button.grid(row=1, column=0, sticky="nsew")

        button2 = tk.Button(self, text="Terminar", command=lambda: send_message('close', 'APP','APP'))
        button2.configure(font='TkFixedFont')
        button2.grid(row=1, column=1, sticky="nsew")

        label2 = tk.Label(self, text="App 1")
        label2.configure(font='TkFixedFont')
        label2.grid(row=2, column=0, sticky="w")

        button3 = tk.Button(self, text="Iniciar", command=lambda: send_message('open', 'APP','APP1'))
        button3.configure(font='TkFixedFont')
        button3.grid(row=3, column=0, sticky="nsew")

        button4 = tk.Button(self, text="Terminar", command=lambda: send_message('close', 'APP','APP1'))
        button4.configure(font='TkFixedFont')
        button4.grid(row=3, column=1, sticky="nsew")

        label3 = tk.Label(self, text="App  2")
        label3.configure(font='TkFixedFont')
        label3.grid(row=4, column=0, sticky="w")

        button5 = tk.Button(self, text="Iniciar", command=lambda: send_message('open', 'APP','APP2'))
        button5.configure(font='TkFixedFont')
        button5.grid(row=5, column=0, sticky="nsew")

        button6 = tk.Button(self, text="Terminar", command=lambda: send_message('close', 'APP','APP2'))
        button6.configure(font='TkFixedFont')
        button6.grid(row=5, column=1, sticky="nsew")

    def build_gui(self):                    
        # Build GUI
        self.root.title('GUI')
        self.root.option_add('*tearOff', 'FALSE')
        self.grid(column=0, row=0, sticky='ew')
        # self.grid_columnconfigure(0, weight=1, uniform='a')
        # self.grid_columnconfigure(1, weight=1, uniform='a')
        # self.grid_columnconfigure(2, weight=1, uniform='a')
        # self.grid_columnconfigure(3, weight=1, uniform='a')

        # Add text widget to display logging info
        label = tk.Label(self, text="Logger")
        label.configure(font='TkFixedFont')
        label.grid(row=1, column=1, sticky="w")

        st = ScrolledText.ScrolledText(self, state='disabled')
        st.configure(font='TkFixedFont')
        st.grid(column=0, row=2, sticky='w', columnspan=3)
        
        button = tk.Button(self, text="Aplicaciones", command=lambda: open_window('apps'))
        button.configure(font='TkFixedFont')
        button.grid(row=3, column=0, sticky="nsew")

        button2 = tk.Button(self, text="Archivos", command=lambda: open_window('file_manager'))
        button2.configure(font='TkFixedFont')
        button2.grid(row=3, column=1, sticky="nsew")

        # Create textLogger
        text_handler = TextHandler(st)

        # Logging configuration
        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s')        

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)

def open_window(wtype):
    window = tk.Tk()
    myGUI(window, wtype)

def connect():
    while True:
        try:
            data = sock.recv(1024)
            if data:
                data = pickle.loads(data)
                if data['codeterm'] == 3:
                    for line in data['data'].split('\n'):
                        logging.info(line)      
        except:
            pass
    

def main():
    global sock
    sock.connect(("localhost", 4000))
    root = tk.Tk()
    myGUI(root, 'main')
    process = threading.Thread(target=connect)
    process.daemon = True
    process.start()
    # send_message('info','FILE','data')
    root.mainloop()

def send_message(process, dst, message):
    global sock
    msg = {'cmd': process, 'src': 'GUI', 'dst': dst, 'msg': message}
    sock.send(pickle.dumps(msg))

if __name__ == '__main__': 
    main()