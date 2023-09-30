import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from sr import speech2text
from send_ip import send
import time, socket, json, threading

# IP Address for PC, SSIP, PORT
PC_IP = '192.168.1.6'
SSIP = '192.168.1.19'
PORT = 8080

# Create an object from class before execute .text() method
receiver = send(SSIP, PORT)

appliances = ['light', 'fan', 'aircon', 'music']
pin = [23, 22, 21, 19]

# Use a dictionary to store appliance statuses
status = {appliance: 0 for appliance in appliances}


class WelcomePage(Screen):

    def __init__(self, **kwargs):
        super(WelcomePage, self).__init__(**kwargs)
        layout = GridLayout(cols=1, rows=3, spacing=10, padding=(10, 20))  # Three rows with spacing and padding

        # Image (first row)
        welcome_image = Image(source='iot_home.jpg')
        layout.add_widget(welcome_image)

        # Big "Welcome" text (second row)
        welcome_label = Label(
            text='IOT Home App',
            font_size='40sp',
            halign='center',
            valign='middle',
        )
        layout.add_widget(welcome_label)

        # BoxLayout for the third row with three boxes
        third_row_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Empty BoxLayout on the left
        third_row_layout.add_widget(BoxLayout())

        # "Enter" button (centered)
        enter_button = Button(text='Enter', size_hint=(None, None), size=(300, 100))
        enter_button.bind(on_press=self.enter_button_press)
        third_row_layout.add_widget(enter_button)

        # Empty BoxLayout on the right
        third_row_layout.add_widget(BoxLayout())

        layout.add_widget(third_row_layout)

        self.add_widget(layout)

    def enter_button_press(self, instance):
        receiver.text('Enter')
        # Switch to the main layout when the "Enter" button is pressed
        App.get_running_app().root.current = 'main_layout'


class MainLayout(Screen):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
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
            on_button.bind(
                on_press=lambda instance, appliance=appliances[i]: self.on_button_press(instance, appliance))
            off_button = Button(text='OFF')
            off_button.bind(
                on_press=lambda instance, appliance=appliances[i]: self.off_button_press(instance, appliance))

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

        self.add_widget(layout)

    # Function for ON Button
    def on_button_press(self, instance, appliance):
        receiver.text(f'turn on the {appliance}')
        print(f"Button ON for {appliance} was pressed!")
        receiver.text('Refresh')

    # Function for OFF Button
    def off_button_press(self, instance, appliance):
        receiver.text(f'turn off the {appliance}')
        print(f"Button OFF for {appliance} was pressed!")
        receiver.text('Refresh')

    # Function for Voice Record Button
    def voice_record_button_press(self, instance):
        print('\nVoice Button Pressed')
        t = speech2text()
        receiver.text(t.get_recognized_text())
        receiver.text('Refresh')

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
                            app = App.get_running_app()
                            screen_manager = app.root
                            for i, appliance in enumerate(appliances):
                                for widget in screen_manager.walk(restrict=True):
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


class GridLayoutApp(App):

    def build(self):
        # Create a ScreenManager to manage multiple screens
        sm = ScreenManager()

        # Welcome Page
        welcome_page = WelcomePage(name='welcome_page')
        sm.add_widget(welcome_page)

        # Main Layout
        main_layout = MainLayout(name='main_layout')
        sm.add_widget(main_layout)

        # Initially, show the welcome page
        sm.current = 'welcome_page'

        return sm


if __name__ == '__main__':
    GridLayoutApp().run()
