import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
from openai import AsyncOpenAI
import asyncio
import threading

# Replace 'your_openai_api_key' with your actual OpenAI API key
OPENAI_API_KEY = '-----------------------'

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
        
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        self.listening = False
        self.loop = asyncio.new_event_loop()
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    # Function to start voice interaction
    def start_voice_interaction(self):
        self.listening = True
        self.text_area.insert(tk.END, "Voice interaction started...\n")
        threading.Thread(target=self.listen).start()
    # Function to stop voice interaction
    def stop_voice_interaction(self):
        self.listening = False
        self.text_area.insert(tk.END, "Voice interaction stopped.\n")
    # Function to listen to user input
    def listen(self):
        if not self.listening:
            return

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
        
        if self.listening:
            self.root.after(1000, self.listen)
    # Function to run async respond
    def run_async_respond(self, user_input):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.respond(user_input))

    async def respond(self, user_input):
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        
        reply = response.choices[0].message.content
        self.text_area.insert(tk.END, f"Chatbot: {reply}\n")
        self.speak(reply)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceChatbotGUI(root)
    root.mainloop()
