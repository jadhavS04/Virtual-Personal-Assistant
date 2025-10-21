import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time
import webbrowser
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading

listener = sr.Recognizer()
machine = pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    try:
        while True:  # Continuously listen for commands
            with sr.Microphone() as source:
                update_status_box("Listening...")  # Update status box
                listener.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
                speech = listener.listen(source, timeout=5)  # Timeout after 5 seconds of silence
                instruction = listener.recognize_google(speech)
                instruction = instruction.lower()
                if "jarvis" in instruction:
                    instruction = instruction.replace('jarvis', '')
                update_status_box("Command: " + instruction)  # Update status box
                return instruction
    except sr.WaitTimeoutError:
        print("Timeout: No command received")
        talk("Please command")
        update_status_box("Please command")  # Update status box
    except Exception as e:
        print(e)
        pass

def update_status_box(text):
    status_box.insert(tk.END, text + "\n")  # Insert text to status box
    status_box.see(tk.END)  # Scroll to the end of status box

def process_command(instruction):
    if "play" in instruction:
        song = instruction.replace('play', '')
        talk("Playing " + song)
        pywhatkit.playonyt(song)
    elif 'time' in instruction:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + current_time)
    elif 'date' in instruction:
        current_date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk("Today's date is " + current_date)
    elif 'how are you' in instruction:
        talk('I am fine, how about you?')
    elif 'what is your name' in instruction:
        talk('I am Jarvis, what can I do for you?')
    elif 'who is' in instruction:
        person = instruction.replace('who is', '')
        try:
            info = wikipedia.summary(person, sentences=3)
            update_status_box("Answer: " + info)  # Update status box
            talk(info)
        except wikipedia.exceptions.DisambiguationError:
            # If multiple pages are found for the search query
            update_status_box("Multiple matches found. Please be more specific.")  # Update status box
            talk("Multiple matches found. Please be more specific.")
        except wikipedia.exceptions.PageError:
            # If the search query does not match any Wikipedia page
            update_status_box("Sorry, I couldn't find any information on that topic.")  # Update status box
            talk("Sorry, I couldn't find any information on that topic.")
    elif 'search' in instruction:
        query = instruction.replace('search', '')
        try:
            talk("Searching for " + query)
            search_url = "https://www.google.com/search?q=" + query
            webbrowser.open(search_url)
        except Exception as e:
            print(e)
            talk("Sorry, I couldn't perform the search at the moment.")
    elif 'welcome our guest' in instruction:
        talk("Welcome everyone to our college science exhibition! We are thrilled to have you all here today to celebrate innovation, creativity, and the wonders of science. Get ready to be amazed by the incredible projects our students have been working on. Let's explore and discover together. Enjoy the exhibition!")
    elif 'exit' in instruction:  # Exit the loop if "exit" command is received
        root.quit()
    else:
        talk('Please repeat')

def Greetings():
    now = time.localtime().tm_hour
    if now >= 3 and now <= 12:
        talk("Good Morning, Sir, Welcome to the Virtual Assistance System Model")
    elif now >= 12 and now <= 17:
        talk("Good Afternoon, Sir, Welcome to the Virtual Assistance System Model")
    elif now >= 17 and now <= 20:
        talk("Good Evening, Sir, Welcome to the Virtual Assistance System Model")
    elif now >= 20 and now <= 24:
        talk("Good Night, Sir, Welcome to the Virtual Assistance System Model")

def setup_gui():
    root = tk.Tk()
    root.title("Jarvis Virtual Assistant")
    root.attributes('-fullscreen', True)  # Open in fullscreen mode

    # Add image
    image_path = r"D:\images\where-is-ai-used-1024x683.jpg"
    image = Image.open(image_path)
    image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    # Resize the image to fit the GUI
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Add status box
    global status_box
    status_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=95, height=45)
    status_box.configure(bg="#000000",fg="#FFFFFF")  # Change background color to a light blue gradient
    status_box.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the status box
    
    return root 

def capture_voice_input():
    while True:
        instruction = input_instruction()
        if instruction:
            process_command(instruction)

# Greetings
threading.Thread(target=Greetings).start()

# Setup GUI
root = setup_gui()

# Start capturing voice input in a separate thread
voice_thread = threading.Thread(target=capture_voice_input)
voice_thread.start()

# Run the Tkinter event loop
root.mainloop()
