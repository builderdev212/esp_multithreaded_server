import tkinter as tk
from tkinter import ttk, scrolledtext, Menu, Spinbox
from tkinter import messagebox as msg
from time import sleep
from client import client, receiver

class gui:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('LED Control')

        self.connection = client()
        self.receiver = receiver()
        self.do_update = False

        self.createWidgets()

    def _quit(self):
        try:
            self.connection.quit()
            self.receiver.quit()
        except:
            pass
        self.win.quit()
        self.win.destroy()
        exit()

    def disconnect(self):
        try:
            self.connection.quit()
            self.receiver.quit()
        except:
            pass

        self.tabs.tab(0, state="normal")
        self.tabs.tab(1, state="disabled")
        self.do_update = False


    def connectToServer(self):
        self.client = self.connection.connect(str(self.ip.get()), int(self.port.get()))

        if self.client == 1:
            msg.showerror('Error', 'Your attempt to connect has failed.')
        elif self.client == 0:
            self.rec = self.receiver.connect(str(self.ip.get()), int(self.port.get()))
            self.tabs.tab(0, state="disabled")
            self.tabs.tab(1, state="normal")
            self.controlLEDTab()
            self.do_update = True

    def rOn(self):
        self.connection.send("a1")

    def rOff(self):
        self.connection.send("a2")

    def bOn(self):
        self.connection.send("a3")

    def bOff(self):
        self.connection.send("a4")

    def updateInfo(self):
        if self.do_update == True:
            output = self.receiver.receive()
            output = str(output)+"\n"

            self.output.configure(state ='normal')
            self.output.insert(tk.INSERT, output)
            self.output.configure(state ='disabled')

            sleep(.1)

        else:
            pass

        self.win.after(1000, self.updateInfo)

    def createWidgets(self):
        self.tabs = ttk.Notebook(self.win)

        self.connectTab = ttk.Frame(self.tabs)
        self.tabs.add(self.connectTab, text='Login')
        self.controlTab = ttk.Frame(self.tabs)
        self.tabs.add(self.controlTab, text='LED Control')

        self.tabs.pack(expand=1, fill="both")

        self.tabs.tab(0, state="normal")
        self.tabs.tab(1, state="disabled")

        self.connectServerTab()
        self.menu()

    def connectServerTab(self):
        # Connect group
        connect = ttk.LabelFrame(self.connectTab, text=' Connect ')
        connect.grid(column=0, row=0, padx=8, pady=4)

        # Labels
        ttk.Label(connect, text="Server IP:").grid(column=0, row=0, padx=2, pady=2)
        ttk.Label(connect, text="Port:").grid(column=0, row=1, padx=2, pady=2)

        # IP entry box
        self.ip = tk.StringVar()
        self.ipEntry = ttk.Entry(connect, width=20, textvariable=self.ip)
        self.ipEntry.grid(column=1, row=0, padx=2, pady=2)

        # Port entry box
        self.port = tk.StringVar()
        self.portEntry = ttk.Entry(connect, width=20, textvariable=self.port)
        self.portEntry.grid(column=1, row=1, padx=2, pady=2)

        # Connect button
        self.connectServer = ttk.Button(connect, text="Connect", command=self.connectToServer)
        self.connectServer.grid(column=0, row=2, padx=2, pady=2, columnspan=2)

    def controlLEDTab(self):
        control = ttk.LabelFrame(self.controlTab, text=' LED Controls ')
        control.grid(column=0, row=0, padx=8, pady=4)

        ttk.Label(control, text="Red LED:").grid(column=0, row=0, padx=2, pady=2)
        ttk.Label(control, text="Blue LED:").grid(column=0, row=1, padx=2, pady=2)

        self.redOn = ttk.Button(control, text="On", command=self.rOn)
        self.redOn.grid(column=1, row=0, padx=2, pady=2)

        self.redOff = ttk.Button(control, text="Off", command=self.rOff)
        self.redOff.grid(column=2, row=0, padx=2, pady=2)

        self.blueOn = ttk.Button(control, text="On", command=self.bOn)
        self.blueOn.grid(column=1, row=1, padx=2, pady=2)

        self.blueOff = ttk.Button(control, text="Off", command=self.bOff)
        self.blueOff.grid(column=2, row=1, padx=2, pady=2)

        self.output = scrolledtext.ScrolledText(control, width=20, height=5, wrap=tk.WORD, state="disabled")
        self.output.grid(column=0, row=2, columnspan=2)

    def menu(self):
        #menu
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)

        #file menu
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Logout", command=self.disconnect)
        fileMenu.add_command(label="Exit", command=self._quit)
        menuBar.add_cascade(label="File", menu=fileMenu)

if __name__ == "__main__":
    gui = gui()
    gui.updateInfo()
    gui.win.mainloop()
