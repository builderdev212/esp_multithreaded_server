import socket
from time import sleep

class client:
    def __init__(self):
        pass

    def connect(self, host, port):
        self.host = host
        self.port = port

        try:
            self.server = socket.socket()
            self.server.connect((self.host, self.port))
            sleep(.1)
            self.server.send("0".encode())
        except:
            return 1
        else:
            return 0

    def send(self, message):
        self.server.send(message.encode())
        sleep(.1)
        data = self.server.recv(32).decode()
        if data == "ack":
            return True
        else:
            return False

    def receive(self):
        return self.server.recv(32).decode()

    def quit(self):
        self.server.close()

class receiver:
    def __init__(self):
        pass

    def connect(self, host, port):
        self.host = host
        self.port = port

        try:
            self.server = socket.socket()
            self.server.connect((self.host, self.port))
            sleep(.1)
            self.server.send("1".encode())
        except:
            return 1
        else:
            return 0

    def receive(self):
        data = self.server.recv(32).decode()

        if data:
            return data
        else:
            pass

    def quit(self):
        self.server.close()
