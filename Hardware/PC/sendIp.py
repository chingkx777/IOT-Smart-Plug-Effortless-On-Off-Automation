import socket
import time

# Define the ESP32's IP address and port
esp32_ip = "192.168.1.22"  # Replace with the ESP32's IP address
esp32_port = 8080  # Choose a port number (e.g., 8080)

# Create a socket for communication
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

time.sleep(2)

try:
    # Connect to the ESP32
    s.connect((esp32_ip, esp32_port))
    
    # Send a message
    message = "turn on the light"
    s.send(message.encode('utf-8'))
    print("Message sent successfully")
    
    # Close the socket
    s.close()
except Exception as e:
    print("Error:", e)
