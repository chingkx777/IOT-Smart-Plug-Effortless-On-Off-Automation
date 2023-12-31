import network
import socket
import time
import json
from machine import Pin, PWM
from oled import oled

# Global Wi-Fi Variable
wifi = network.WLAN(network.STA_IF)

# Define your Wi-Fi credentials
ssid = 'YOUR SSID'
password = 'YOUR PASSWORD'

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
            time.sleep(1)
            i += 1
            print(f'Connecting to Wi-Fi......{i}s')
            oled([
                ["Waiting for", 20],
                [f"Wi-Fi...{i}s", 30]
                  ])
        
        print("\nConnected to Wi-Fi")
        self.ip = f'{wifi.ifconfig()[0]}'
        
        # Specify the file name
        file_name = "ip_address.txt"

        # Open the file in write mode
        with open(file_name, "w") as file:
            # Write the IP address to the file
            file.write(self.ip)

        # Close the file
        file.close()

        # LED 2 turn on when Wi-Fi is connected
        led2 = PWM(Pin(2))
        led2.freq(1000)
        led2.duty(100)
        
        # Create a socket server to receive messages
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        
    def text(self):
        # Bind Server
        self.server.bind(('0.0.0.0', self.receiver_port))
        print('Server is listening on port', self.receiver_port)
        
        # Receive and print the message
        data, addr = self.server.recvfrom(1024)
        message = data.decode()
        print(f'\nReceived message {addr}: {message}')
        
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
            message = f'Data sent to {self.receiver_ip}: {data_to_send}'
            print(message)
            
            # Reset list to initial state
            data_to_send.clear()
            
        except Exception as e:
            print('Error:', e)
