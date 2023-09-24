import socket

class send:
    def __init__(self, ip, port):
        # Define Message, ESP32's IP address and port
        self.ip = ip  # Replace with the ESP32's IP address
        self.port = port  # Choose a port number (e.g., 8080)

    def text(self, message):
        word = str(message)

        # Create a socket for communication
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Connect to the ESP32
            s.connect((self.ip, self.port))
            
            # Send a message
            s.send(word.encode())
            print("Message sent successfully\n")
            
            # Close the socket
            s.close()
        except Exception as e:
            print("Error:", e)