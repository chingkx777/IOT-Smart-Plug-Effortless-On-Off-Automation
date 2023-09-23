import network
import socket
import time

# Global Wi-Fi Variable
wifi = network.WLAN(network.STA_IF)

# Define your Wi-Fi credentials
ssid = 'SSID'
password = 'PASSWORD'

class Sync:
    def __init__(self, receiver_port):
        # Define the port on which the receiver should listen
        self.receiver_port = receiver_port

        # Connect to Wi-Fi
        wifi.active(True)
        wifi.connect(ssid, password)

        # Wait for Wi-Fi connection
        while not wifi.isconnected():
            pass

        print("\nConnected to Wi-Fi")
        print(f'IP: {wifi.ifconfig()}')
        
        # Create a socket server to receive messages
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('0.0.0.0', self.receiver_port))
        print("Server is listening on port", self.receiver_port)

    
    def text(self):
        # Receive and print the message
        data, addr = self.server.recvfrom(1024)
        message = data.decode()
        print(f"\nReceived message {addr}: {message}")
        return message

    
    def close(self):
        self.server.close()
        wifi.disconnect()

# Creating Object from Class, and then run method
# t = SyncR(8080)
# while True:
#     t.text()
