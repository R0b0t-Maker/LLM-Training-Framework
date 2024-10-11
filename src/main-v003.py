import tkinter as tk  # GUI framework
from tkinter import ttk  # Themed Tkinter widgets
from tkinter import scrolledtext  # Provides scrollable text widget
import speech_recognition as sr  # Library for speech recognition
import pyttsx3  # Library for text-to-speech
from openai import AsyncOpenAI  # OpenAI API for GPT model interaction
import asyncio  # Used to run asynchronous tasks
import threading  # For running tasks in parallel threads

# Replace 'your_openai_api_key' with your actual OpenAI API key
OPENAI_API_KEY = '-----------------------------'  # API Key to authenticate with OpenAI

class VoiceChatbotGUI:
    def __init__(self, root):
        """Initialize the VoiceChatbotGUI with the main window, widgets, and components."""
        self.root = root
        self.root.title("Advanced Voice Chatbot")  # Set the window title
        self.root.geometry("900x750")  # Define window dimensions

        # Configure style for the widgets
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")  # Frame background
        style.configure("TLabel", font=("Helvetica", 14), background="#f0f0f0")  # Label font
        style.configure("TButton", font=("Helvetica", 12), padding=10)  # Button style
        style.configure("TScrolledText", font=("Helvetica", 12))  # ScrolledText widget font

        # Main frame to hold all components
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header Label
        self.header_label = ttk.Label(self.main_frame, text="Advanced Voice Chatbot", font=("Helvetica", 18, "bold"))
        self.header_label.pack(pady=10)

        # Scrollable text area to display conversation
        self.text_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=70, height=15, font=("Helvetica", 12))
        self.text_area.pack(pady=20, padx=20)

        # Button Frame to hold control buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        # Start button to initiate voice interaction
        self.start_button = ttk.Button(self.button_frame, text="Start Voice Interaction", command=self.start_voice_interaction, style="Accent.TButton")
        self.start_button.grid(row=0, column=0, padx=10)

        # Stop button to halt voice interaction
        self.stop_button = ttk.Button(self.button_frame, text="Stop Voice Interaction", command=self.stop_voice_interaction, style="Accent.TButton")
        self.stop_button.grid(row=0, column=1, padx=10)

        # Settings frame for speech speed and voice gender
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack(pady=10)

        # Speed slider to control speech rate
        self.speed_label = ttk.Label(self.settings_frame, text="Speed:")
        self.speed_label.grid(row=0, column=0, padx=5)
        self.speed_slider = ttk.Scale(self.settings_frame, from_=50, to=300, orient=tk.HORIZONTAL)
        self.speed_slider.set(150)  # Default speech rate
        self.speed_slider.grid(row=0, column=1, padx=5)

        # Voice gender selection dropdown
        self.voice_gender_label = ttk.Label(self.settings_frame, text="Voice Gender:")
        self.voice_gender_label.grid(row=1, column=0, padx=5)
        self.voice_gender_combobox = ttk.Combobox(self.settings_frame, values=["Male", "Female"], state="readonly")
        self.voice_gender_combobox.set("Male")  # Default to Male voice
        self.voice_gender_combobox.grid(row=1, column=1, padx=5)

        # Canvas to show visual wave animation for speech
        self.wave_canvas = tk.Canvas(self.main_frame, width=800, height=100, bg="#f0f0f0", bd=0, highlightthickness=0, relief='ridge')
        self.wave_canvas.pack(pady=20)

        # Initialize speech recognition and synthesis components
        self.engine = pyttsx3.init()  # Text-to-speech engine
        self.recognizer = sr.Recognizer()  # Speech recognition engine
        self.microphone = sr.Microphone()  # Microphone for input

        self.listening = False  # Flag to track voice interaction status
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)  # Initialize OpenAI client

    def start_voice_interaction(self):
        """Start the voice interaction and activate the listening thread."""
        self.listening = True
        self.text_area.insert(tk.END, "Voice interaction started...\n")
        threading.Thread(target=self.listen).start()  # Start listening in a separate thread

    def stop_voice_interaction(self):
        """Stop the voice interaction."""
        self.listening = False
        self.text_area.insert(tk.END, "Voice interaction stopped.\n")

    def listen(self):
        """Capture the user's voice input and process it."""
        if not self.listening:
            return

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust microphone for ambient noise
            self.text_area.insert(tk.END, "Listening...\n")
            audio = self.recognizer.listen(source)  # Listen for input

        try:
            user_input = self.recognizer.recognize_google(audio)  # Convert speech to text using Google API
            self.text_area.insert(tk.END, f"User: {user_input}\n")
            threading.Thread(target=self.run_async_respond, args=(user_input,)).start()  # Handle response in another thread
        except sr.UnknownValueError:
            self.text_area.insert(tk.END, "Sorry, I did not understand that.\n")
        except sr.RequestError:
            self.text_area.insert(tk.END, "Request error.\n")

        if self.listening:
            self.root.after(1000, self.listen)  # Continue listening after a delay

    def run_async_respond(self, user_input):
        """Run the response function asynchronously."""
        asyncio.run(self.respond(user_input))  # Use asyncio to manage the asynchronous response

    async def respond(self, user_input):
        """Send user input to OpenAI GPT model and process the response."""
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]  # Send user input to OpenAI API
        )
        
        reply = response.choices[0].message.content  # Extract the reply from OpenAI
        self.text_area.insert(tk.END, f"Chatbot: {reply}\n")
        self.speak(reply)  # Speak the chatbot's response
        self.animate_wave()  # Show animation for voice response

    def speak(self, text):
        """Convert text to speech using pyttsx3."""
        self.engine.setProperty('rate', self.speed_slider.get())  # Set speech rate

        voices = self.engine.getProperty('voices')
        if self.voice_gender_combobox.get() == "Male":
            self.engine.setProperty('voice', voices[0].id)  # Set male voice
        else:
            self.engine.setProperty('voice', voices[1].id)  # Set female voice

        self.engine.say(text)  # Speak the text
        self.engine.runAndWait()

    def animate_wave(self):
        """Animate the wave visualization on the canvas."""
        self.wave_canvas.delete("wave")  # Clear previous wave drawings
        width = self.wave_canvas.winfo_width()
        height = self.wave_canvas.winfo_height()

        for x in range(0, width, 10):
            y = height // 2 + 20 * (-1) ** (x // 10)  # Create alternating wave pattern
            self.wave_canvas.create_oval(x, y, x + 10, y + 10, fill="blue", outline="", tags="wave")

        self.root.after(100, self.animate_wave)  # Continue animation

# Entry point for the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main Tkinter window
    app = VoiceChatbotGUI(root)  # Instantiate the chatbot GUI
    root.mainloop()  # Run the application event loop
