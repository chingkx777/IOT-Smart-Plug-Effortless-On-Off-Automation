# When using this, make sure your SpeechRecognition & Pyaudio package being installed
import speech_recognition as sr

class speech2text():
    def __init__(self):
        # Create an object from class
        self.recognized_text = None
        r = sr.Recognizer()

        # Open your source mic and record
        with sr.Microphone() as source:
            print('\n********************************')
            print('Start recording......\n')
            audio = r.listen(source, timeout=4, phrase_time_limit=3)

            # Speech to Text using Google API
            try:
                text = r.recognize_google(audio)
                print(f"Message: {text}\n")
                self.recognized_text = text
            except:
                print('Sorry, could not recognize your voice\n')

    def get_recognized_text(self):
        return self.recognized_text
