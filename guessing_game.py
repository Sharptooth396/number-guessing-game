import random
import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import urllib.request
import shutil

# --- Auto-updater ---
CURRENT_VERSION = "1.0.3"
EXE_URL = "https://raw.githubusercontent.com/Sharptooth396/number-guessing-game/main/guessing_game.exe"
VERSION_URL = "https://raw.githubusercontent.com/Sharptooth396/number-guessing-game/main/version"

def check_for_update():
    try:
        latest_version = urllib.request.urlopen(VERSION_URL).read().decode().strip()
        if latest_version > CURRENT_VERSION:
            if messagebox.askyesno("Update Available", f"New version {latest_version} available. Update now?"):
                urllib.request.urlretrieve(EXE_URL, "guessing_game_new.exe")
                messagebox.showinfo("Update Downloaded", "Update downloaded! Restart to apply.")
                os.rename(sys.executable, "guessing_game_old.exe")
                shutil.move("guessing_game_new.exe", sys.executable)
                sys.exit()
    except Exception as e:
        print(f"Update check failed: {e}")

# Load progress
def load_progress():
    global exp, level
    if os.path.exists('savegame.txt'):
        with open('savegame.txt', 'r') as file:
            exp, level = map(int, file.read().split(','))
    else:
        exp, level = 0, 1

# Save progress
def save_progress():
    with open('savegame.txt', 'w') as file:
        file.write(f"{exp},{level}")

# Calculate level based on EXP
def update_level():
    global level
    level = exp // 133 + 1

# Reset game for new round
def reset_game():
    global number, guesses, attempts
    number = random.randint(1, 100)
    guesses = []
    attempts = 0
    game_frame.pack_forget()
    guesses_label.config(text="Your guesses: []")
    hint_label.config(text="")
    feedback_label.config(text="")
    attempts_label.config(text="")
    difficulty_frame.pack(pady=20)
    update_level()
    medium_btn.config(state='normal' if level >= 20 else 'disabled')
    hard_btn.config(state='normal' if level >= 30 else 'disabled')
    save_progress()

# Set game difficulty
def set_difficulty(mode):
    global attempts, max_attempts
    if mode == 'Easy':
        attempts = max_attempts = 15
    elif mode == 'Medium':
        attempts = max_attempts = 10
    else:
        attempts = max_attempts = 5
    attempts_label.config(text=f"Attempts left: {attempts}")
    difficulty_frame.pack_forget()
    game_frame.pack(pady=20)

# Check player's guess
def check_guess():
    global attempts, exp
    guess = int(entry.get())
    guesses.append(guess)
    attempts -= 1

    guesses_label.config(text=f"Your guesses: {guesses}")
    attempts_label.config(text=f"Attempts left: {attempts}")

    if guess == number:
        exp += 40
        update_level()
        messagebox.showinfo("Congratulations!", f"You guessed it! The number was {number}.\nEXP: {exp}\nLevel: {level}")
        reset_game()
    elif attempts == 0:
        messagebox.showinfo("You Lose!", f"You lost! The number was {number}.")
        reset_game()
    elif guess < number:
        feedback_label.config(text="Too low!", fg="#e06c75")
    else:
        feedback_label.config(text="Too high!", fg="#61afef")

# Display hint
def show_hint():
    hint = "even" if number % 2 == 0 else "odd"
    hint_label.config(text=f"Hint: The number is {hint}!")

# Hint button action
def hint_button_action():
    show_hint()

window = tk.Tk()
window.title("Number Guessing Game")
window.configure(bg="#282c34")
window.geometry('400x420')

# Difficulty selection frame
difficulty_frame = tk.Frame(window, bg='#282c34')
difficulty_frame.pack(expand=True)
tk.Label(difficulty_frame, text="Select Difficulty", bg="#282c34", fg="#ffffff", font=("Arial", 14)).pack(pady=10)
tk.Button(difficulty_frame, text="Easy", command=lambda: set_difficulty('Easy'), bg="#61afef", fg="#ffffff", width=10).pack(pady=5)
medium_btn = tk.Button(difficulty_frame, text="Medium", command=lambda: set_difficulty('Medium'), bg="#98c379", fg="#ffffff", width=10)
medium_btn.pack(pady=5)
hard_btn = tk.Button(difficulty_frame, text="Hard", command=lambda: set_difficulty('Hard'), bg="#e06c75", fg="#ffffff", width=10)
hard_btn.pack(pady=5)

# Main game frame
game_frame = tk.Frame(window, bg='#3c4048')
game_frame.pack(expand=True)
label = tk.Label(game_frame, text="I'm thinking of a number (1-100)", bg="#3c4048", fg="#ffffff", font=("Arial", 12))
label.pack(pady=10)

hint_label = tk.Label(game_frame, text="", bg="#3c4048", fg="#abb2bf", font=("Arial", 10))
hint_label.pack(pady=5)

entry = tk.Entry(game_frame, font=("Arial", 10), justify='center')
entry.pack(pady=5)

button = tk.Button(game_frame, text="Guess", command=check_guess, bg="#56b6c2", fg="#ffffff", width=10)
button.pack(pady=5)

hint_button = tk.Button(game_frame, text="Show Hint", command=hint_button_action, bg="#c678dd", fg="#ffffff", width=10)
hint_button.pack(pady=5)

feedback_label = tk.Label(game_frame, text="", bg="#3c4048", fg="#ffffff", font=("Arial", 10))
feedback_label.pack(pady=5)

attempts_label = tk.Label(game_frame, text="Attempts left: ", bg="#3c4048", fg="#ffffff", font=("Arial", 10))
attempts_label.pack(pady=5)

guesses_label = tk.Label(game_frame, text="Your guesses: []", bg="#3c4048", fg="#ffffff", font=("Arial", 10))
guesses_label.pack(pady=5)

# Version label at bottom
version_label = tk.Label(window, text=f"Version: {CURRENT_VERSION}", bg="#282c34", fg="#ffffff", font=("Arial", 9))
version_label.pack(side='bottom', pady=5)

load_progress()
check_for_update()
reset_game()
window.mainloop()
