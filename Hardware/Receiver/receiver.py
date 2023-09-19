import network
import socket
import time

# Define your Wi-Fi credentials
ssid = "HUAWEI nova 7"
password = "nova7140720"

# Define the port on which the receiver should listen
receiver_port = 8080  # Use the same port number as in the sender

# Create a socket server to receive messages
def create_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', receiver_port))
    server.listen(1)
    print("Server is listening on port", receiver_port)
    return server

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
print(wifi.ifconfig())

# Wait for Wi-Fi connection
while not wifi.isconnected():
    pass

print("Connected to Wi-Fi")

# Create the server
server = create_server()

# Main loop to handle incoming connections
while True:
    try:
        conn, addr = server.accept()
        print("Connected by", addr)
        
        # Receive and print the message
        message = conn.recv(1024).decode('utf-8')
        print("Received message:", message)
        
        # Handle the received message as needed
        
        # Close the connection
        conn.close()
    except Exception as e:
        print("Error:", e)
