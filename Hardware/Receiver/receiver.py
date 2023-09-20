import network
import socket
import time

# Global Wi-Fi Variable
wifi = network.WLAN(network.STA_IF)

# Define your Wi-Fi credentials
ssid = "HUAWEI nova 7"
password = "nova7140720"

class SyncR:
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
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', self.receiver_port))
        self.server.listen(1)
        print("Server is listening on port", self.receiver_port)

        
        
    def text(self):
        # Handle incoming connections
        conn, addr = self.server.accept()
        print("Connected by", addr)
                
        # Receive and print the message
        message = conn.recv(1024).decode('utf-8')
        print("Received message:", message)
                
        # Close the connection, server & Wi-Fi
        conn.close()
        self.server.close()
        time.sleep(1)
        wifi.disconnect()
        
        # Return message receive
        return message

# Creating Object from Class, and then run method
# t = SyncR(8080)
# t.text()
