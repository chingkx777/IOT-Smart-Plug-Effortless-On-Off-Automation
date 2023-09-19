import network
import socket
import time

# Define your Wi-Fi credentials
ssid = "HUAWEI nova 7"
password = "nova7140720"

# Define the IP address and port of the receiver ESP32
receiver_ip = "192.168.43.120"
receiver_port = 8080  # Choose a port number (e.g., 8080)

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

# Wait for Wi-Fi connection
while not wifi.isconnected():
    pass

print("Connected to Wi-Fi")

# Create a socket for communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the receiver
    s.connect((receiver_ip, receiver_port))
    
    # Send a message
    message = "Hello, ESP32 receiver!"
    s.send(message.encode('utf-8'))
    print("Message sent successfully")
    
    # Close the socket
    s.close()
except Exception as e:
    print("Error:", e)

# Disconnect from Wi-Fi
wifi.disconnect()
