#Need more comments
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
from openai import AsyncOpenAI
import asyncio
import threading

#need API to run the code
OPENAI_API_KEY = '---------------------'
#class for the GUI
class VoiceChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice Chatbot")
        
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Arial", 12))
        self.text_area.pack(pady=20)
        
        self.start_button = tk.Button(root, text="Start Voice Interaction", command=self.start_voice_interaction)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Voice Interaction", command=self.stop_voice_interaction)
        self.stop_button.pack(pady=10)
        
        self.stop_voice_button = tk.Button(root, text="Stop Voice Output", command=self.stop_voice_output)
        self.stop_voice_button.pack(pady=10)
        
        self.read_last_response_button = tk.Button(root, text="Read Last Response", command=self.read_last_response)
        self.read_last_response_button.pack(pady=10)
        
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        self.listening = False
        self.voice_active = True
        self.speaking = False
        self.last_response = ""
        self.loop = asyncio.new_event_loop()
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    #function to setup the voice
    def setup_voice(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "english" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1)
    #function to start voice interaction
    def start_voice_interaction(self):
        self.listening = True
        self.text_area.insert(tk.END, "Voice interaction started...\n")
        threading.Thread(target=self.listen).start()
    #function to stop voice interaction
    def stop_voice_interaction(self):
        self.listening = False
        self.text_area.insert(tk.END, "Voice interaction stopped.\n")
    #function to stop voice output
    def stop_voice_output(self):
        self.engine.stop()
        self.speaking = False
        self.voice_active = False
        self.text_area.insert(tk.END, "Voice output stopped.\n")
    #function to read the last response
    def read_last_response(self):
        if self.last_response:
            self.speak(self.last_response)
    #function to listen to user input
    def listen(self):
        while self.listening:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.text_area.insert(tk.END, "Listening...\n")
                audio = self.recognizer.listen(source)
            
            try:
                user_input = self.recognizer.recognize_google(audio)
                self.text_area.insert(tk.END, f"User: {user_input}\n")
                threading.Thread(target=self.run_async_respond, args=(user_input,)).start()
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "Sorry, I did not understand that.\n")
            except sr.RequestError:
                self.text_area.insert(tk.END, "Request error.\n")
    
    def run_async_respond(self, user_input):
        asyncio.run(self.respond(user_input))

    async def respond(self, user_input):
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        self.last_response = response.choices[0].message.content
        self.text_area.insert(tk.END, f"Chatbot: {self.last_response}\n")
        if self.voice_active:
            self.speak(self.last_response)

    def speak(self, text):
        if not self.speaking:
            self.speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.speaking = False

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceChatbotGUI(root)
    root.mainloop()
