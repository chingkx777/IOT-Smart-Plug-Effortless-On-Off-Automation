import network
import socket
import time

# Global Object for Wi-Fi
wifi = network.WLAN(network.STA_IF)

# Global Object for UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class SyncS:
    def __init__(self, receiver_ip, receiver_port):
        # Define SSID and Password
        self.ssid = "HUAWEI nova 7"
        self.password = "nova7140720"

        # Define the IP address and port of the receiver ESP32
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port  # Choose a port number 

        # Connect to Wi-Fi
        wifi.active(True)
        wifi.connect(self.ssid, self.password)

        # Wait for Wi-Fi connection
        while not wifi.isconnected():
            pass

        print("Connected to Wi-Fi")

    
    def text(self, message):
        # Connect to the receiver
        udp_socket.connect((self.receiver_ip, self.receiver_port))
            
        # Send a message
        udp_socket.send(message.encode('utf-8'))
        print("Message sent successfully")
            
        # Close the socket
        udp_socket.close()
        
        # Disconnect from Wi-Fi
        wifi.disconnect()

# Creating Object from Class, and then run method
# ESP1 = SyncS('192.168.43.16', 8080)
# ESP1.text('Hi, ESP')
