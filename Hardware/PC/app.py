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
from kivy.uix.popup import Popup

# IP Address for PC, SSIP, PORT
PC_IP = 'YOUR PC_IP'
SSIP = 'YOUR SSIP'
PORT = 8000

# Create an object from class before execute .text() method
receiver = send(SSIP, PORT)

appliances = ['light', 'fan', 'charger']
pin = [23, 22, 21]

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
        receiver.text('stop')
        receiver.text('task_1')
        receiver.text('enter')
        # Switch to the main layout when the "Enter" button is pressed
        App.get_running_app().root.current = 'main_layout'


class MainLayout(Screen):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        layout = GridLayout(cols=3, rows=len(appliances) + 3, spacing=10, padding=10)

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

        # Get the size_hint of the individual buttons
        button_size_hint = (None, None)

        # Add "Voice Record" button to the first column
        voice_record_button = Button(text='Voice Record', size_hint=button_size_hint)
        voice_record_button.size = (320, 100)  # Set the size directly
        voice_record_button.bind(on_press=self.voice_record_button_press)
        layout.add_widget(voice_record_button)

        # Add "All On" button with the same size as individual buttons to the second column
        all_on_button = Button(text='All On', size_hint=button_size_hint)
        all_on_button.size = (320, 100)  # Set the size directly
        all_on_button.bind(on_press=self.all_on_button_press)
        layout.add_widget(all_on_button)

        # Add "All Off" button with the same size as individual buttons to the third column
        all_off_button = Button(text='All Off', size_hint=button_size_hint)
        all_off_button.size = (320, 100)  # Set the size directly
        all_off_button.bind(on_press=self.all_off_button_press)
        layout.add_widget(all_off_button)

        exit_button = Button(text='Exit')
        exit_button.bind(on_press=self.exit_button_press)
        layout.add_widget(Label())  # Empty widget for the left column
        layout.add_widget(exit_button)
        layout.add_widget(Label())  # Empty widget for the right column

        # Start a thread to listen for UDP messages and update statuses
        self.listen_thread = threading.Thread(target=self.listen_for_udp_messages)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.add_widget(layout)

    # Function for ON Button
    def on_button_press(self, instance, appliance):
        receiver.text('task_1')
        receiver.text(f'turn on the {appliance}')
        print(f"Button ON for {appliance} was pressed!")
        time.sleep(0.5)
        receiver.text('Refresh')

    # Function for OFF Button
    def off_button_press(self, instance, appliance):
        receiver.text('task_1')
        receiver.text(f'turn off the {appliance}')
        print(f"Button OFF for {appliance} was pressed!")
        time.sleep(0.5)
        receiver.text('Refresh')

    # Function for Voice Record Button
    def voice_record_button_press(self, instance):
        receiver.text('task_1')
        print('\nVoice Button Pressed')
        t = speech2text()
        receiver.text(t.get_recognized_text())
        receiver.text('refresh')

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
                    print('OK')

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

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
        except Exception as e:
            print(f"Error listening for UDP messages: {e}")
    
    def add_all_on_off_buttons(self, layout):
        # All On button (centered)
        all_on_button = Button(text='All On', size_hint=(None, None), size=(300, 100))
        all_on_button.bind(on_press=self.all_on_button_press)
        layout.add_widget(all_on_button)

        # All Off button (centered)
        all_off_button = Button(text='All Off', size_hint=(None, None), size=(300, 100))
        all_off_button.bind(on_press=self.all_off_button_press)
        layout.add_widget(all_off_button)

    def all_on_button_press(self, instance):
        receiver.text('task_1')
        receiver.text('everything on')
        print("Button ON for ALL was pressed!")
        time.sleep(0.5)
        receiver.text('Refresh')

    def all_off_button_press(self, instance):
        receiver.text('task_1')
        receiver.text('everything off')
        print("Button OFF for ALL was pressed!")
        time.sleep(0.5)
        receiver.text('Refresh')

    def exit_button_press(self, instance):
        # Create a popup confirmation dialog before exiting
        confirm_popup = Popup(title='Exit Confirmation', size_hint=(None, None), size=(400, 200))

        # Create a horizontal BoxLayout for buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Add Yes and No buttons to the BoxLayout
        yes_button = Button(text='Yes', size_hint=(None, None), size=(100, 50))
        no_button = Button(text='No', size_hint=(None, None), size=(100, 50))

        # Bind the functions to the Yes and No buttons
        yes_button.bind(on_press=self.exit_app)
        no_button.bind(on_press=confirm_popup.dismiss)

        # Add buttons to the BoxLayout
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)

        # Add the BoxLayout to the popup content
        confirm_popup.content = button_layout

        # Open the popup
        confirm_popup.open()

    def exit_app(self, instance):
        print('Closing App......')
        receiver.text('task_2')
        # Function to exit the application
        App.get_running_app().stop()


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
