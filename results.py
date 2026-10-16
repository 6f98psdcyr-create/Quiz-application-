"""Result screen for the quiz game."""
import tkinter as tk
from styles import BG, PANEL, PANEL_ALT, CYAN, PURPLE, PINK, TEXT, MUTED, GREEN, YELLOW, FONT

class ResultsScreen:
    def __init__(self, parent, score, total, correct, wrong, timed_out, on_replay, on_exit):
        self.parent = parent
        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build(score, total, correct, wrong, timed_out, on_replay, on_exit)

    def _build(self, score, total, correct, wrong, timed_out, on_replay, on_exit):
        percent = round((score / total) * 100) if total else 0
        if percent >= 80:
            headline, accent = "EXCELLENT WORK!", GREEN
            message = "Outstanding performance. Keep challenging yourself!"
        elif percent >= 50:
            headline, accent = "GOOD EFFORT!", CYAN
            message = "You're making progress. Review the explanations and try again."
        else:
            headline, accent = "KEEP PRACTICING!", PINK
            message = "Every attempt is practice. Replay to improve your score."

        tk.Label(self.frame, text="QUIZ COMPLETE", bg=BG, fg=PURPLE,
                 font=(FONT, 10, "bold")).pack(pady=(34, 5))
        tk.Label(self.frame, text=headline, bg=BG, fg=accent,
                 font=(FONT, 26, "bold")).pack()
        tk.Label(self.frame, text=message, bg=BG, fg=MUTED,
                 font=(FONT, 10), wraplength=530).pack(pady=(8, 22))

        card = tk.Frame(self.frame, bg=PANEL, highlightbackground=accent, highlightthickness=1)
        card.pack(padx=36, fill="x")
        tk.Label(card, text="YOUR SCORE", bg=PANEL, fg=MUTED,
                 font=(FONT, 10, "bold")).pack(pady=(18, 0))
        tk.Label(card, text=f"{score} / {total}", bg=PANEL, fg=TEXT,
                 font=(FONT, 36, "bold")).pack()
        tk.Label(card, text=f"{percent}% accuracy", bg=PANEL, fg=accent,
                 font=(FONT, 14, "bold")).pack(pady=(0, 18))

        stats = tk.Frame(self.frame, bg=BG)
        stats.pack(fill="x", padx=36, pady=18)
        for label, value, color in [
            ("CORRECT", correct, GREEN), ("INCORRECT", wrong, PINK),
            ("TIMED OUT", timed_out, YELLOW)
        ]:
            cell = tk.Frame(stats, bg=PANEL_ALT, padx=8, pady=12)
            cell.pack(side="left", expand=True, fill="x", padx=5)
            tk.Label(cell, text=str(value), bg=PANEL_ALT, fg=color,
                     font=(FONT, 21, "bold")).pack()
            tk.Label(cell, text=label, bg=PANEL_ALT, fg=MUTED,
                     font=(FONT, 8, "bold")).pack()

        tk.Button(self.frame, text="↻  PLAY AGAIN", command=on_replay,
                  bg=CYAN, fg=BG, activebackground="#8AF3FF", activeforeground=BG,
                  relief="flat", cursor="hand2", font=(FONT, 11, "bold"),
                  padx=22, pady=11, bd=0).pack(pady=(8, 10))
        tk.Button(self.frame, text="EXIT GAME", command=on_exit,
                  bg=BG, fg=MUTED, activebackground=BG, activeforeground=TEXT,
                  relief="flat", cursor="hand2", font=(FONT, 10, "bold"),
                  padx=18, pady=7, bd=0).pack()
