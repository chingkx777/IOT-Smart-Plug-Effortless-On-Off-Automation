import network
import socket
import time
import json

# Global Wi-Fi Variable
wifi = network.WLAN(network.STA_IF)

# Define your Wi-Fi credentials
ssid = 'SSID'
password = 'PASSWORD'

class Sync:
    def __init__(self, receiver_ip, receiver_port):
        # Define the ip and port on which the receiver should listen
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port

        # Connect to Wi-Fi
        wifi.active(True)
        wifi.connect(ssid, password)

        # Wait for Wi-Fi connection
        i = 0
        while not wifi.isconnected():
            print(f'\nConnecting to Wi-Fi......{i}s')
            time.sleep(1)
            i += 1

        print("\nConnected to Wi-Fi")
        print(f'IP: {wifi.ifconfig()}')
        
        # Create a socket server to receive messages
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        
    def text(self):
        # Bind Server
        self.server.bind(('0.0.0.0', self.receiver_port))
        print("Server is listening on port", self.receiver_port)
        
        # Receive and print the message
        data, addr = self.server.recvfrom(1024)
        message = data.decode()
        print(f"\nReceived message {addr}: {message}")
        
        return message
    
    
    def close(self):
        self.server.close()
        wifi.disconnect()
      
      
    def status(self, status_list):
        try:
            # Data to be sent (a list)
            data_to_send = status_list

            # Serialize the list to JSON and encode as bytes
            json_data = json.dumps(data_to_send)
            data_bytes = json_data.encode('utf-8')

            # Send the JSON data to the PC
            self.server.sendto(data_bytes, (self.receiver_ip, self.receiver_port))
            message = f"Data sent: {data_to_send}"
            print(message)
            
            # Reset list to initial state
            data_to_send.clear()
            
        except Exception as e:
            print("Error:", e)
