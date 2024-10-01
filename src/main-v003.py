#add comments for the code
#Add the API for the code

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
from openai import AsyncOpenAI
import asyncio
import threading

# Replace 'your_openai_api_key' with your actual OpenAI API key
OPENAI_API_KEY = '-----------------------------'

class VoiceChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Voice Chatbot")
        self.root.geometry("900x750")

        # Configure style
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", font=("Helvetica", 14), background="#f0f0f0")
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TScrolledText", font=("Helvetica", 12))

        # Main Frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self.header_label = ttk.Label(self.main_frame, text="Advanced Voice Chatbot", font=("Helvetica", 18, "bold"))
        self.header_label.pack(pady=10)

        # Text area
        self.text_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 12))
        self.text_area.pack(pady=20, padx=20)

        # Button Frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        # Start button
        self.start_button = ttk.Button(self.button_frame, text="Start Voice Interaction", command=self.start_voice_interaction, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=10)

        # Stop button
        self.stop_button = ttk.Button(self.button_frame, text="Stop Voice Interaction", command=self.stop_voice_interaction, style="Accent.TButton")
        self.stop_button.grid(row=0, column=1, padx=10)

        # Settings Frame
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack(pady=10)

        # Speed label and slider
        self.speed_label = ttk.Label(self.settings_frame, text="Speed:")
        self.speed_label.grid(row=0, column=0, padx=5)
        self.speed_slider = ttk.Scale(self.settings_frame, from_=50, to=300, orient=tk.HORIZONTAL)
        self.speed_slider.set(150)  # Default speed
        self.speed_slider.grid(row=0, column=1, padx=5)

        # Voice gender label and combobox
        self.voice_gender_label = ttk.Label(self.settings_frame, text="Voice Gender:")
        self.voice_gender_label.grid(row=1, column=0, padx=5)
        self.voice_gender_combobox = ttk.Combobox(self.settings_frame, values=["Male", "Female"], state="readonly")
        self.voice_gender_combobox.set("Male")  # Default gender
        self.voice_gender_combobox.grid(row=1, column=1, padx=5)

        # Wave Canvas
        self.wave_canvas = tk.Canvas(self.main_frame, width=800, height=100, bg="#f0f0f0", bd=0, highlightthickness=0, relief='ridge')
        self.wave_canvas.pack(pady=20)

        # Initialize speech components
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.listening = False
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
        asyncio.run(self.respond(user_input))

    async def respond(self, user_input):
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        
        reply = response.choices[0].message.content
        self.text_area.insert(tk.END, f"Chatbot: {reply}\n")
        self.speak(reply)
        self.animate_wave()

    def speak(self, text):
        self.engine.setProperty('rate', self.speed_slider.get())

        voices = self.engine.getProperty('voices')
        if self.voice_gender_combobox.get() == "Male":
            self.engine.setProperty('voice', voices[0].id)  # Male voice
        else:
            self.engine.setProperty('voice', voices[1].id)  # Female voice

        self.engine.say(text)
        self.engine.runAndWait()

    def animate_wave(self):
        self.wave_canvas.delete("wave")
        width = self.wave_canvas.winfo_width()
        height = self.wave_canvas.winfo_height()
        
        for x in range(0, width, 10):
            y = height // 2 + 20 * (-1) ** (x // 10)  # Alternating wave pattern
            self.wave_canvas.create_oval(x, y, x + 10, y + 10, fill="blue", outline="", tags="wave")
        
        self.root.after(100, self.animate_wave)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceChatbotGUI(root)
    root.mainloop()
