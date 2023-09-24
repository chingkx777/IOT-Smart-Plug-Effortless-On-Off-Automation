import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from sr import speech2text
from send_ip import send
import time, socket, json, threading

# IP Address for PC, SSIP, PORT
PC_IP = 'PC'
SSIP = 'SSIP'
PORT = 7777

# Create an object from class before execuete .text() method
receiver = send(SSIP, PORT)

appliances = ['light', 'fan', 'aircon', 'music']
pin = [23, 22, 21, 19]

# Use a dictionary to store appliance statuses
status = {appliance: 0 for appliance in appliances}

class GridLayoutApp(App):

    def build(self):
        layout = GridLayout(cols=3, rows=6, spacing=10, padding=10)
        
        # First row
        # Left column (empty)
        layout.add_widget(Label())

        # Middle column with text display (centered)
        text_display = Label(
            text='IOT Home APP',
            font_size='20sp',
            halign='center',  # Center text horizontally
            valign='middle',  # Center text vertically
        )
        layout.add_widget(text_display)

        # Right column (empty)
        layout.add_widget(Label())

        # Middle rows
        for i in range(len(appliances)):
            # Create a grid layout for each appliance
            appliance_row = GridLayout(cols=2, spacing=10)

            # Label for pin
            label_text = Label(text=f'Pin {pin[i]}:\n{appliances[i].upper()}')
            label_text.appliance_name = appliances[i]
            appliance_row.add_widget(label_text)

            # Image for status
            image_input = Image(source='off.png') if status[appliances[i]] == 0 else Image(source='on.png')
            image_input.appliance_name = appliances[i]
            appliance_row.add_widget(image_input)

            # ON and OFF buttons
            on_button = Button(text='ON')
            on_button.bind(on_press=lambda instance, appliance=appliances[i]: self.on_button_press(instance, appliance))
            off_button = Button(text='OFF')
            off_button.bind(on_press=lambda instance, appliance=appliances[i]: self.off_button_press(instance, appliance))

            # Bind the source property of the Image widget to the status dictionary
            image_input.bind(source=self.update_image_source)

            # Add appliance row and buttons to the main layout
            layout.add_widget(appliance_row)
            layout.add_widget(on_button)
            layout.add_widget(off_button)

        # Last row with a button in the middle column
        layout.add_widget(Label())  # Empty widget for the left column
        voice_record_button = Button(text='Voice Record')
        voice_record_button.bind(on_press=self.voice_record_button_press)
        layout.add_widget(voice_record_button)
        layout.add_widget(Label())  # Empty widget for the right column

        # Start a thread to listen for UDP messages and update statuses
        self.listen_thread = threading.Thread(target=self.listen_for_udp_messages)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        return layout


    # Function for ON Button
    def on_button_press(self, instance, appliance):
        receiver.text(f'turn on the {appliance}')
        print(f"Button ON for {appliance} was pressed!")


    # Function for OFF Button
    def off_button_press(self, instance, appliance):
        receiver.text(f'turn off the {appliance}')
        print(f"Button OFF for {appliance} was pressed!")


    # Function for Voice Record Button
    def voice_record_button_press(self, instance):
        print('\nVoice Button Pressed')
        t = speech2text()
        receiver.text(t.get_recognized_text())
        time.sleep(2)


    # Change ON/OFF png according to Dictionary Statuses
    def update_image_source(self, instance, value):
        appliance = instance.appliance_name
        if value == 'on.png':
            status[appliance] = 1
        else:
            status[appliance] = 0


    # Listen Pin Status from ESP32
    def listen_for_udp_messages(self):
        try:
            # Create a UDP socket to listen for messages from ESP32
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind((PC_IP, PORT))
                print(f"Listening on ({PC_IP}, {PORT})")

                while True:
                    data, addr = sock.recvfrom(1024)

                    try:
                        # Parse the received JSON data as a list
                        received_data = json.loads(data.decode('utf-8'))
                        print(f"Received data from {addr}: {received_data}")

                        # Update appliance statuses based on the received list
                        for i, status_value in enumerate(received_data):
                            status[appliances[i]] = status_value

                        # Update the UI in the main thread using Kivy's Clock.schedule_once
                        def update_ui_in_main_thread(dt):
                            for i, appliance in enumerate(appliances):
                                for widget in self.root.walk(restrict=True):
                                    if isinstance(widget, Image) and hasattr(widget, 'appliance_name') and widget.appliance_name == appliance:
                                        if status[appliance] == 1:
                                            widget.source = 'on.png'
                                        else:
                                            widget.source = 'off.png'

                        kivy.clock.Clock.schedule_once(update_ui_in_main_thread)

                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON data: {e}")

        except Exception as e:
            print(f"Error listening for UDP messages: {e}")

if __name__ == '__main__':
    GridLayoutApp().run()
