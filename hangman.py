import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd
import time
import datetime
import os

# Load or create player stats file
STATS_FILE = "hangman_stats.csv"
if not os.path.exists(STATS_FILE):
    df = pd.DataFrame(columns=["Player", "Word", "Result", "AttemptsUsed", "Date"])
    df.to_csv(STATS_FILE, index=False)

# Sample words categorized
WORDS = {
    "Animals": ["tiger", "elephant", "giraffe", "kangaroo", "dolphin"],
    "Programming": ["python", "compiler", "algorithm", "function", "debug"],
    "Food": ["pizza", "burger", "biryani", "sushi", "sandwich"],
    "Sports": ["cricket", "football", "tennis", "badminton", "hockey"]
}

class FuturisticHangman:
    def __init__(self, master):
        self.master = master
        self.master.title("🌌 Futuristic Hangman 3000 🌌")
        self.master.geometry("700x600")
        self.master.configure(bg="black")

        self.stats_df = pd.read_csv(STATS_FILE)

        self.setup_homepage()

    def setup_homepage(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="🌌 WELCOME TO FUTURISTIC HANGMAN 3000 🌌", font=("Consolas", 18, "bold"), fg="#00ffff", bg="black").pack(pady=40)

        tk.Label(self.master, text="Enter Your Name:", font=("Consolas", 14), fg="white", bg="black").pack()
        self.entry_name = tk.Entry(self.master, font=("Consolas", 14), bg="#111", fg="#0f0")
        self.entry_name.pack(pady=10)

        tk.Button(self.master, text="Start Game", font=("Consolas", 14), command=self.choose_category, bg="#00ffcc").pack(pady=10)
        tk.Button(self.master, text="View Leaderboard", font=("Consolas", 14), command=self.show_leaderboard, bg="#ffaa00").pack(pady=10)

    def choose_category(self):
        self.player_name = self.entry_name.get()
        if not self.player_name:
            messagebox.showwarning("Name Required", "Please enter your name.")
            return

        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Choose Category:", font=("Consolas", 16), fg="#ffcc00", bg="black").pack(pady=20)
        for category in WORDS:
            tk.Button(self.master, text=category, font=("Consolas", 14), bg="#444", fg="white", command=lambda c=category: self.choose_difficulty(c)).pack(pady=5)

    def choose_difficulty(self, category):
        self.category = category
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"Category: {category}", font=("Consolas", 14), fg="cyan", bg="black").pack(pady=10)
        tk.Label(self.master, text="Choose Difficulty:", font=("Consolas", 16), fg="white", bg="black").pack(pady=20)

        tk.Button(self.master, text="Easy", font=("Consolas", 14), command=lambda: self.start_game(10), bg="#66ff66").pack(pady=5)
        tk.Button(self.master, text="Medium", font=("Consolas", 14), command=lambda: self.start_game(6), bg="#ffcc00").pack(pady=5)
        tk.Button(self.master, text="Hard", font=("Consolas", 14), command=lambda: self.start_game(5), bg="#ff6666").pack(pady=5)

    def start_game(self, attempts):
        self.word = random.choice(WORDS[self.category])
        self.display_word = ["_" for _ in self.word]
        self.used_letters = []
        self.attempts_left = attempts
        self.total_attempts = attempts
        self.hints_used = 0
        self.max_hints = 2
        self.start_time = time.time()
        self.update_game_ui()

    def update_game_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text=f"{self.player_name} vs. AI", font=("Consolas", 14), fg="#ff00ff", bg="black").pack(pady=5)
        tk.Label(self.master, text=f"Category: {self.category}  |  Attempts Left: {self.attempts_left}", font=("Consolas", 12), fg="white", bg="black").pack()
        self.hint_label = tk.Label(self.master, text=f"Hints used: {self.hints_used}/{self.max_hints}", fg="white", bg="black", font=("Consolas", 12))
        self.hint_label.pack()

        tk.Label(self.master, text=" ".join(self.display_word), font=("Consolas", 40), fg="#00ffcc", bg="black").pack(pady=20)
        tk.Label(self.master, text=f"Used Letters: {', '.join(self.used_letters)}", font=("Consolas", 12), fg="yellow", bg="black").pack()

        self.entry_guess = tk.Entry(self.master, font=("Consolas", 20), bg="#222", fg="lime", width=5)
        self.entry_guess.pack(pady=10)

        btn_frame = tk.Frame(self.master, bg="black")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Guess", bg="#00ffe7", font=("Consolas", 14), command=self.make_guess).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Hint", bg="#ffdf00", font=("Consolas", 14), command=self.use_hint).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Quit", bg="#ff0000", fg="white", font=("Consolas", 14), command=self.setup_homepage).pack(side="left", padx=10)

    def make_guess(self):
        guess = self.entry_guess.get().lower()

        if not guess or len(guess) != 1 or not guess.isalpha():
            return

        if guess in self.used_letters:
            return

        self.used_letters.append(guess)

        if guess in self.word:
            for i, char in enumerate(self.word):
                if char == guess:
                    self.display_word[i] = guess
        else:
            self.attempts_left -= 1

        if "_" not in self.display_word:
            self.end_game("Win")
        elif self.attempts_left <= 0:
            self.end_game("Lose")
        else:
            self.update_game_ui()

    def use_hint(self):
        if self.hints_used >= self.max_hints:
            return

        self.hints_used += 1
        hint_letter = self.word[0] if self.hints_used == 1 else random.choice([c for c in self.word if c not in self.display_word])

        for i, char in enumerate(self.word):
            if char == hint_letter:
                self.display_word[i] = hint_letter

        self.update_game_ui()

    def end_game(self, result):
        time_taken = int(time.time() - self.start_time)
        messagebox.showinfo("Game Over", f"You {result}! The word was '{self.word}'")

        attempts_used = self.total_attempts - self.attempts_left
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        new_row = pd.DataFrame([[self.player_name, self.word, result, attempts_used, date]], columns=self.stats_df.columns)
        self.stats_df = pd.concat([self.stats_df, new_row], ignore_index=True)
        self.stats_df.to_csv(STATS_FILE, index=False)

        self.show_achievements(result, attempts_used)

    def show_achievements(self, result, attempts_used):
        achievement = ""
        wins = self.stats_df[(self.stats_df.Player == self.player_name) & (self.stats_df.Result == "Win")]

        if result == "Win":
            if self.attempts_left == 1:
                achievement = "🏆 Comeback King!"
            elif attempts_used <= 3:
                achievement = "⏱️ Fast Finisher!"
            if len(wins) >= 10:
                achievement += " 🌟 Word Wizard!"

        msg = f"{achievement}\n\nPlay Again?"
        if messagebox.askyesno("Achievement Unlocked", msg):
            self.choose_category()
        else:
            self.setup_homepage()

    def show_leaderboard(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="🏆 Leaderboard 🏆", font=("Consolas", 18), fg="gold", bg="black").pack(pady=20)
        top_players = self.stats_df[self.stats_df.Result == "Win"].groupby("Player").size().sort_values(ascending=False).head(5)

        for name, wins in top_players.items():
            tk.Label(self.master, text=f"{name}: {wins} Wins", font=("Consolas", 14), fg="#00ffcc", bg="black").pack()

        tk.Button(self.master, text="Back", font=("Consolas", 14), command=self.setup_homepage, bg="gray").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticHangman(root)
    root.mainloop()
