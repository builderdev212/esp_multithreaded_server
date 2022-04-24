import socket
import threading
from time import sleep

class server:
    """
    This server is used to communicate between controllers and esps.
    It acts a go between on the local network, and in this case I am hosting
    it from my raspberry pi, although it could be hosted from any computer.
    """
    def __init__(self, ip, port):
        """
        This starts the server and listens for new connections from clients.
        When a new client connects it creates a thread for that client based on the id
        it sends.
        """
        self.server = socket.socket()
        self.response = None # This is to be used for communication between the controller and the esps.
        self.is_info = None

        print('Server started!')
        print('Waiting for clients...')

        self.server.bind((ip, port)) # Bind the server to the host and port chosen in the initiation of the server.
        self.server.listen(5) # Listen for connections to the server.

        while True:
           client, addr = self.server.accept() # Wait for a client to connect.
           new_client = threading.Thread(target=self.on_new_client, args=(client, addr))
           new_client.start() # Create and start a new thread for the client if a client is connected.

        self.server.close() # Close the server.
        print('Server stopped.')

    def on_new_client(self, client, addr):
        """
        This is the thread created for a client whenever a new client is connected.
        After the connection, it must send the server an id, so that the server knows what to do
        with that client. Otherwise, the client will be shutdown.
        """
        sleep(0.1)
        msg = client.recv(32).decode() # Reads the id.

        if msg == "0": # If the client identifies as a controller.
            print("Controller connected at {}!".format(addr[0]))
            self.controller(client, addr) # Starts the loop for the controller.
            print("Controller at {} disconnected.".format(addr[0]))
        if msg == "1": # If the client identifies as a reciever.
            print("Receiver connected at {}!".format(addr[0]))
            self.receiver(client, addr) # Starts the loop for the reciever.
            print("Receiver at {} disconnected.".format(addr[0]))
        elif msg == "a": # If the client identifies as esp a.
            print("Esp A connected at {}!".format(addr[0]))
            self.espa(client, addr) # Starts the loop for esp a.
            print("Esp A at {} disconnected.".format(addr[0]))
        elif msg == "b": # If the client identifies as esp b.
            print("Esp B connected at {}!".format(addr[0]))
            self.espb(client, addr) # Starts the loop for esp b.
            print("Esp B at {} disconnected.".format(addr[0]))
        else: # If the client doesn't send an ID or gives an invalid id.
            print("Error: Client connected didn't send id to server or id sent was invalid.")

        client.close() # Closes the connection to the client when finished.

    def controller(self, client, addr):
        """
        This is the loop ran if a controller is connected. In this case, the controller is only sending data,
        and not receiving any information.
        """
        while True:
            self.data = client.recv(32).decode() # Reads the data.
            # Data should be formatted as "a1" where the first character, a, tells the server what esp to send the command(the numbers afterwords).

            if not self.data:
                break # If there is no more data being read stop.

            elif self.data:
                esp_num = self.data[0] # The esp id.
                self.cmd = self.data[1::] # The command.

                if esp_num == "a":
                    self.response = "a" # This will be noticed by the espa loop if one is connected.
                    sleep(0.2) # This waits for the esp to do it's things with the command sent.

                    if self.response == "ack": # If successful,
                        client.send("ack".encode()) # Tell the client it was successful.
                    else:
                        client.send("fail".encode()) # Else, tell the client it was unsuccessful.

                    self.response = None # Set the response back to None.
                else:
                    pass
            else:
                break # If this even comes up than there is an issue and it should stop.

    def espa(self, client, addr):
        """
        This is the loop ran if esp a is connected. This is looking for self.respone to be set to "a".
        """
        while True:
            if self.response == "a": # If there is a command to be sent to esp a.
                client.send(self.cmd.encode()) # Send the command.
                sleep(0.1)
                self.response = client.recv(32).decode() # Listen for the response and set self.response to the response.
                sleep(0.1)
            else:
                pass

    def espb(self, client, addr):
        while True:
            self.info = client.recv(32).decode()

            if not self.info:
                break
            elif self.info:
                self.is_info = True

            sleep(0.5)

    def receiver(self, client, addr):
        while True:
            if self.is_info == True:
                client.send(self.info.encode())
                self.is_info = None
                sleep(0.1)
            else:
                pass

            sleep(0.1)
