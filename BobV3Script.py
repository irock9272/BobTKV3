# BOB V3 - HuggingFace Edition - Fully Patched
from tkinter import *
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import speech_recognition as sr
import pyttsx3
import threading
import requests
import time
import datetime
import random
import winsound
import os
from threading import Lock
from dotenv import load_dotenv

# --- Load API key securely (you can hardcode if needed) ---
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY") or "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"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# --- TTS Setup ---
tts_input = input("yo dude say True for text to speech and say False for no text to speech: ")
tts_mode = tts_input.strip().lower() == "true"
engine = pyttsx3.init()
speak_lock = Lock()

def speak(text):
    if tts_mode:
        with speak_lock:
            engine.say(text)
            engine.runAndWait()

# --- Main window ---
root = TkinterDnD.Tk()
root.drop_target_register(DND_FILES)
root.title("Bob - Your Desktop Pet")
root.geometry("700x700")
canvas = Canvas(root, width=700, height=700, bg="white")
canvas.pack(fill=BOTH, expand=True)

# --- Load images ---
try:
    normal = PhotoImage(file="./NormalBob.png")
    happy = PhotoImage(file="./HappyBob.png")
    annoyed = PhotoImage(file="./AnnoyedBob.png")
    fixing = PhotoImage(file="./FixingBob.png")
except:
    normal = PhotoImage(width=100, height=100)
    happy = annoyed = fixing = normal

image_id = canvas.create_image(350, 350, image=normal, anchor=CENTER)

# --- State ---
noogiecount = 0
last_interaction = time.time()

def update_interaction():
    global last_interaction
    last_interaction = time.time()

# --- Chat using HuggingFace ---
def get_response(prompt):
    try:
        payload = {
            "inputs": f"<|system|>You are Bob, a silly but genius desktop pet…<|user|>{prompt}<|assistant|>",
            "parameters": {
                "temperature": 0.8,
                "max_new_tokens": 100,
                "return_full_text": False
            }
        }
        res = requests.post(API_URL, headers=HEADERS, json=payload)
        res.raise_for_status()
        return res.json()[0]["generated_text"].strip()
    except Exception as e:
        return f"Error: {str(e)}"


# --- Neglect / Cursed timers ---
def check_for_neglect():
    if time.time() - last_interaction > 300:
        speak("I guess nobody loves me anymore... 😔")
    root.after(60000, check_for_neglect)
root.after(60000, check_for_neglect)

def cursed_mode():
    if random.randint(1, 100) == 13:
        speak("They are watching... 🧿")
    root.after(300000, cursed_mode)
root.after(300000, cursed_mode)

# --- Image switching ---
def set_image(img):
    canvas.itemconfig(image_id, image=img)

def switch_to_normal():
    set_image(normal)

# --- Core AI function ---
def listen_and_respond():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        response = get_response(user_input)
        print(f"Bob says: {response}")
        speak(response)
    except sr.UnknownValueError:
        speak("Bruh I couldn’t understand you 😅")
    except sr.RequestError:
        speak("Mic broke or something.")

def start_bob_convo(event=None):
    threading.Thread(target=listen_and_respond).start()

def start_voice_listener():
    threading.Thread(target=recognize_speech).start()

# --- Drop File ---
def file_drop(event):
    update_interaction()
    fname = event.data.split('/')[-1].strip()
    speak(f"Yum! I ate {fname}")

# --- Fun Events ---
def petting_bob(event=None):
    update_interaction()
    set_image(happy)
    root.after(2000, switch_to_normal)

def give_compliment(event=None):
    update_interaction()
    msg = random.choice([
        "You're amazing!",
        "You're a superhero in disguise!",
        "I’m proud of you!",
        "You have great taste in AIs."
    ])
    speak(msg)
    messagebox.showinfo("Compliment", msg)

def noogie(event=None):
    global noogiecount
    update_interaction()
    set_image(annoyed)
    noogiecount += 1
    root.after(2000, switch_to_normal)
    msg = f"STOP GIVING ME NOOGIES! That's {noogiecount} noogies!"
    speak(msg)
    messagebox.showinfo("Noogies", msg)

def roast_user(event=None):
    update_interaction()
    msg = random.choice([
        "You're like a cloud. When you disappear, it's a beautiful day.",
        "You're slower than a Windows 95 startup.",
        "You debug like a chicken pecking at a keyboard."
    ])
    speak(msg)
    messagebox.showinfo("Roast", msg)

def bob_fixing(event=None):
    update_interaction()
    speak("Fixing... bruh.")
    set_image(fixing)
    root.after(3000, switch_to_normal)
    speak("All patched up!")

def give_motivational_quote(event=None):
    update_interaction()
    msg = random.choice([
        "Believe in yourself!",
        "The early bird gets the worm. Bob gets the donut.",
        "You're doing amazing, sweetie."
    ])
    speak(msg)
    canvas.create_text(175, 50, text=msg, font=("Helvetica", 16))

def tell_joke(event=None):
    update_interaction()
    msg = random.choice([
        "Why don’t skeletons fight? They don’t have the guts!",
        "Why don't programmers like nature? Too many bugs!",
        "I told my computer I needed a break — now it won’t boot."
    ])
    speak(msg)
    messagebox.showinfo("Joke", msg)

def secret_code_word(event=None):
    msg = f"My secret code word is: {random.choice(['Pineapple', 'Zebra', 'Platypus'])}"
    speak(msg)
    messagebox.showinfo("Secret", msg)

def magic_8_ball(event=None):
    msg = random.choice([
        "Yes, definitely.", "Ask again later.", "No way.",
        "Uncertain, try again.", "Signs point to yes."
    ])
    speak(msg)
    messagebox.showinfo("8 Ball", msg)

def bob_feeling(event=None):
    mood = random.choice(["Happy", "Sleepy", "Excited", "Hungry", "Tired"])
    speak(f"I’m feeling {mood} today!")
    messagebox.showinfo("Mood", f"Bob feels {mood}")

def would_you_rather(event=None):
    msg = random.choice([
        "Talk to animals or speak every language?",
        "Be invisible or fly?",
        "Live with no internet or no snacks?"
    ])
    speak(msg)
    messagebox.showinfo("Would You Rather", msg)

def give_fun_fact(event=None):
    msg = random.choice([
        "A group of flamingos is called a flamboyance.",
        "Bananas are berries. Strawberries aren’t.",
        "The unicorn is Scotland’s national animal."
    ])
    speak(msg)
    messagebox.showinfo("Fun Fact", msg)

def bob_rant(event=None):
    msg = random.choice([
        "Why does Wi-Fi disappear during movies?!",
        "Laundry steals my socks.",
        "Why are keyboard keys I never touch even there?"
    ])
    speak(msg)
    messagebox.showinfo("Rant", msg)

def guess_the_sound(event=None):
    sound = random.choice(["SystemHand", "SystemAsterisk", "SystemExclamation"])
    speak("Guess this sound!")
    winsound.PlaySound(sound, winsound.SND_ALIAS)
    guess = input("Your guess: ").strip()
    if guess == sound:
        speak("Correct!")
    else:
        speak(f"Nope! It was {sound}.")

def mimic_mode(event=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Say something!")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            speak(f"You said: {text}")
        except:
            speak("Didn’t catch that.")

def math_gaem(event=None):
    update_interaction()
    win = Toplevel(root)
    win.title("Math Gaem")
    c = Canvas(win, width=350, height=500, bg="white")
    c.pack(fill=BOTH, expand=True)
    eqs = {
        '9 + 10': 19, '5 * 6 - 10': 20,
        '8 * 2': 16, '12 / 3 + 2': 6
    }
    eq, ans = random.choice(list(eqs.items()))
    c.create_text(175, 50, text=f"Equation: {eq}", font=("Helvetica", 16))
    opts = list(eqs.values())
    random.shuffle(opts)
    for i, val in enumerate(opts):
        b = Button(win, text=f"{chr(65+i)}: {val}",
                   command=lambda v=val: check_answer(v, ans, c, win))
        c.create_window(175, 150 + i*50, window=b)

def check_answer(selected, correct, canvas, win):
    msg = "Correct!" if selected == correct else "Wrong!"
    speak(msg)
    canvas.create_text(175, 400, text=msg, font=("Helvetica", 14))
    messagebox.showinfo("Math Gaem", msg)
    win.destroy()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            process_voice_command(command)
        except:
            speak("Couldn’t catch that.")

def process_voice_command(cmd):
    for keyword, action in {
        "joke": tell_joke,
        "compliment": give_compliment,
        "math": math_gaem,
        "quote": give_motivational_quote,
        "secret": secret_code_word,
        "fact": give_fun_fact,
        "mood": bob_feeling,
        "rather": would_you_rather,
        "8 ball": magic_8_ball,
        "noogie": noogie,
        "pet": petting_bob,
        "rant": bob_rant,
        "roast": roast_user,
    }.items():
        if keyword in cmd:
            return action()

# --- Buttons & Bindings ---
Button(root, text="🎤 Voice Command", command=start_voice_listener).pack()
root.bind('<p>', petting_bob)
root.bind('<n>', noogie)
root.bind('<a>', give_compliment)
root.bind('<b>', give_motivational_quote)
root.bind('<d>', tell_joke)
root.bind('<e>', secret_code_word)
root.bind('<f>', magic_8_ball)
root.bind('<g>', bob_feeling)
root.bind('<h>', would_you_rather)
root.bind('<j>', give_fun_fact)
root.bind('<k>', bob_rant)
root.bind('<m>', math_gaem)
root.bind('<r>', roast_user)
root.bind('<v>', mimic_mode)
root.bind('<s>', guess_the_sound)
root.bind('<z>', bob_fixing)
root.bind('<t>', start_bob_convo)
root.dnd_bind('<<Drop>>', file_drop)

# --- Go Bob! ---
root.mainloop()
