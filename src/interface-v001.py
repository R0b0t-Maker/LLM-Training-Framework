import tkinter as tk
from tkinter import messagebox

# Define the questions and options
questions = [
    "What are some activities you enjoy doing in your free time?",
    "Do you enjoy reading? If yes, what kinds of books or stories do you like?",
    "How do you like to start your mornings?",
    "Do you prefer having quiet conversations or more lively discussions?",
    "What are some things that make you happy?",
    "Is there anything that often makes you feel worried or anxious?",
    "Can you tell me about your daily routine?",
    "When during the day do you feel you need more company or assistance?",
    "What kind of music do you enjoy listening to?",
    "What kinds of TV shows or movies do you like to watch?",
    "Do you do any physical activities or exercises regularly?",
    "Are there any health topics you would like more information about?",
    "Do you prefer short chats or longer, more detailed conversations?",
    "How often would you like me to check in with you?",
    "What kind of help would you like with daily tasks?"
]

options = [
    ["Reading books or stories", "Gardening or taking care of plants", "Watching TV shows or movies", "Knitting, crocheting, or other crafts", "Playing board games or solving puzzles"],
    ["Yes, I love fiction like mysteries or romances", "Yes, I enjoy non-fiction like biographies or history", "Yes, I like reading newspapers or magazines", "Yes, I prefer listening to audiobooks", "No, I don't read much"],
    ["Going for a gentle walk or doing some light exercise", "Having a quiet breakfast with a cup of tea or coffee", "Reading the newspaper or watching the morning news", "Enjoying a hobby like knitting or gardening", "Talking with family or friends"],
    ["I prefer quiet, relaxed conversations", "I enjoy lively, engaging discussions", "I like a mix of both, depending on the day", "It varies based on how I feel"],
    ["Spending time with family or friends", "Listening to my favorite music", "Completing a craft or project", "Being outdoors in nature", "Learning something new or interesting"],
    ["Concerns about my health", "Feeling lonely or isolated", "Worries about finances", "Uncertainty about the future", "Challenges with using technology"],
    ["Morning activities (e.g., breakfast, exercise)", "Afternoon activities (e.g., hobbies, socializing)", "Evening activities (e.g., dinner, TV)", "Nighttime routine (e.g., reading, preparing for bed)"],
    ["In the mornings", "During the afternoons", "In the evenings", "At night", "It changes from day to day"],
    ["Classical music", "Jazz", "Pop/Rock music", "Country music", "A variety of different types"],
    ["Comedies that make me laugh", "Dramas with interesting stories", "Documentaries about real-life topics", "Action or adventure movies", "I enjoy watching the news"],
    ["I like to go for walks", "I do yoga or gentle stretching", "I enjoy swimming or water exercises", "I do exercises that are suitable for limited mobility", "I am interested in starting but need some guidance"],
    ["Healthy eating and nutrition", "Managing chronic health conditions", "Mental health and emotional well-being", "Exercise and staying active", "I'm open to learning about different health topics"],
    ["I prefer short, friendly chats", "I enjoy longer, more detailed conversations", "It depends on the topic we're discussing", "I don't have a preference"],
    ["Several times a day", "Once a day", "Every few days", "Once a week", "Only when I ask for it"],
    ["Reminders to take my medication", "Reminders about appointments", "Finding information or answering questions", "Help with using technology", "Tips and advice for daily living"]
]

responses = [{} for _ in range(len(questions))]

root = tk.Tk()
root.title("Personal Companion Questionnaire")
root.geometry("800x600")
root.configure(bg='#f0f4f7')

current_question = 0

def next_question():
    global current_question
    if current_question < len(questions):
        question_label.config(text=questions[current_question])
        for i, option in enumerate(options[current_question]):
            buttons[i].config(text=option, variable=vars[i], onvalue=option, offvalue="")
            buttons[i].pack(anchor="w", padx=20, pady=5)
        for i in range(len(options[current_question]), len(buttons)):
            buttons[i].pack_forget()
        prev_button.pack(side="left", padx=20, pady=20)
        next_button.pack(side="right", padx=20, pady=20)
        skip_button.pack(side="right", padx=20, pady=20)
    else:
        show_summary()

def record_response():
    global current_question
    selected_options = [var.get() for var in vars if var.get()]
    responses[current_question] = {questions[current_question]: selected_options}
    current_question += 1
    next_question()

def skip_question():
    global current_question
    responses[current_question] = {questions[current_question]: []}
    current_question += 1
    next_question()

def prev_question():
    global current_question
    if current_question > 0:
        current_question -= 1
    next_question()

def show_summary():
    summary = "Thank you! Here are your responses:\n\n"
    for i, question in enumerate(questions):
        summary += f"{question}\nAnswer: {', '.join(responses[i].get(question, []))}\n\n"
    messagebox.showinfo("Summary", summary)
    root.quit()

def show_welcome_screen():
    welcome_frame = tk.Frame(root, bg='#f0f4f7')
    welcome_frame.pack(fill="both", expand=True)
    welcome_label = tk.Label(welcome_frame, text="Welcome to Your Personal Companion!", font=("Helvetica", 24, "bold"), bg='#f0f4f7', fg='#333333')
    welcome_label.pack(pady=40)
    intro_label = tk.Label(welcome_frame, text="We're here to get to know you better so we can make our conversations more meaningful and helpful. Let's start with a few questions about your preferences.", wraplength=700, font=("Helvetica", 16), bg='#f0f4f7', fg='#555555')
    intro_label.pack(pady=20)
    start_button = tk.Button(welcome_frame, text="Start Questionnaire", command=lambda: [welcome_frame.destroy(), display_questionnaire()], font=("Helvetica", 14), bg='#4CAF50', fg='white', activebackground='#45a049')
    start_button.pack(pady=20)

def display_questionnaire():
    question_label.pack(pady=20)
    for button in buttons:
        button.pack(anchor="w", padx=20, pady=5)
    button_frame.pack(side="bottom", fill="x", pady=20)
    next_question()

question_label = tk.Label(root, text="", font=("Helvetica", 18), wraplength=700, bg='#f0f4f7', fg='#333333')

vars = [tk.StringVar() for _ in range(5)]
buttons = [tk.Checkbutton(root, text="", variable=var, onvalue=var, offvalue="", font=("Helvetica", 14), wraplength=700, bg='#f0f4f7', fg='#555555', selectcolor='#f0f4f7', activebackground='#f0f4f7') for var in vars]

button_frame = tk.Frame(root, bg='#f0f4f7')

next_button = tk.Button(button_frame, text="Next", command=record_response, font=("Helvetica", 14), bg='#4CAF50', fg='white', activebackground='#45a049')
prev_button = tk.Button(button_frame, text="Previous", command=prev_question, font=("Helvetica", 14), bg='#4CAF50', fg='white', activebackground='#45a049')
skip_button = tk.Button(button_frame, text="Skip", command=skip_question, font=("Helvetica", 14), bg='#4CAF50', fg='white', activebackground='#45a049')

# Pack buttons in the button_frame
prev_button.pack(side="left", padx=20)
skip_button.pack(side="right", padx=20)
next_button.pack(side="right", padx=20)

show_welcome_screen()

root.mainloop()
