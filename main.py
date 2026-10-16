"""Entry point for the Neon Quiz Application."""
import json
import random
import tkinter as tk
from tkinter import messagebox
from quiz import QuizScreen
from results import ResultsScreen
from styles import BG, PANEL, CYAN, PURPLE, TEXT, MUTED, FONT

QUESTION_COUNT = 10
SECONDS_PER_QUESTION = 15
QUESTIONS_FILE = "questions.json"

class NeonQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Quiz | Python Edition")
        self.root.geometry("620x720")
        self.root.minsize(540, 650)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        self.current_screen = None
        self.show_welcome()

    def load_questions(self):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                bank = json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            messagebox.showerror("Question file error",
                                 f"Could not load {QUESTIONS_FILE}.\n\n{exc}")
            return []
        if len(bank) < QUESTION_COUNT:
            messagebox.showerror("Not enough questions",
                                 f"Add at least {QUESTION_COUNT} questions to {QUESTIONS_FILE}.")
            return []
        random.shuffle(bank)
        selected = bank[:QUESTION_COUNT]
        for question in selected:
            if not all(key in question for key in ("question", "options", "answer")):
                messagebox.showerror("Invalid question data",
                                     "Each question needs question, options, and answer fields.")
                return []
            if len(question["options"]) != 4 or question["answer"] not in question["options"]:
                messagebox.showerror("Invalid question data",
                                     "Each question must have four options and an answer matching one option.")
                return []
        return selected

    def show_welcome(self):
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None
        frame = tk.Frame(self.root, bg=BG)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="PYTHON PROJECT  /  01", bg=BG, fg=PURPLE,
                 font=(FONT, 9, "bold")).pack(pady=(75, 14))
        tk.Label(frame, text="NEON", bg=BG, fg=CYAN,
                 font=(FONT, 42, "bold")).pack()
        tk.Label(frame, text="QUIZ ARENA", bg=BG, fg=TEXT,
                 font=(FONT, 25, "bold")).pack(pady=(0, 8))
        tk.Label(frame, text="Think fast. Choose wisely. Beat your best score.",
                 bg=BG, fg=MUTED, font=(FONT, 10), wraplength=400).pack(pady=(0, 30))

        info = tk.Frame(frame, bg=PANEL, highlightbackground="#29345C", highlightthickness=1)
        info.pack(fill="x", padx=55)
        for label, value in [
            ("QUESTIONS", "10"), ("TIME PER QUESTION", "15 SEC"), ("DIFFICULTY", "MIXED")
        ]:
            row = tk.Frame(info, bg=PANEL)
            row.pack(fill="x", padx=18, pady=10)
            tk.Label(row, text=label, bg=PANEL, fg=MUTED,
                     font=(FONT, 9, "bold")).pack(side="left")
            tk.Label(row, text=value, bg=PANEL, fg=CYAN,
                     font=(FONT, 10, "bold")).pack(side="right")
        tk.Label(frame, text="SCORING  •  +1 for each correct answer  •  No negative marks",
                 bg=BG, fg=MUTED, font=(FONT, 9), wraplength=460).pack(pady=22)
        tk.Button(frame, text="▶   START QUIZ", command=self.start_quiz,
                  bg=CYAN, fg=BG, activebackground="#8AF3FF", activeforeground=BG,
                  relief="flat", bd=0, cursor="hand2", font=(FONT, 12, "bold"),
                  padx=32, pady=13).pack()
        tk.Label(frame, text="GENERAL KNOWLEDGE  +  PROGRAMMING  +  COMPUTER SCIENCE",
                 bg=BG, fg="#5C668A", font=(FONT, 8, "bold")).pack(side="bottom", pady=25)
        self.current_screen = frame

    def start_quiz(self):
        questions = self.load_questions()
        if not questions:
            return
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = QuizScreen(self.root, questions, SECONDS_PER_QUESTION, self.show_results)

    def show_results(self, score, total, correct, wrong, timed_out):
        self.current_screen = ResultsScreen(
            self.root, score, total, correct, wrong, timed_out,
            on_replay=self.start_quiz, on_exit=self.exit_game
        )

    def exit_game(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    NeonQuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
