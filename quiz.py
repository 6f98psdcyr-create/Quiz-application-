"""Quiz gameplay screen: questions, answer validation, navigation and timer."""
import tkinter as tk
import random
from styles import BG, PANEL, PANEL_ALT, CYAN, PURPLE, PINK, TEXT, MUTED, GREEN, RED, YELLOW, FONT

class QuizScreen:
    def __init__(self, parent, questions, seconds_per_question, on_finish):
        self.parent = parent
        self.questions = questions
        self.seconds_per_question = seconds_per_question
        self.on_finish = on_finish
        self.index = 0
        self.score = 0
        self.correct = 0
        self.wrong = 0
        self.timed_out = 0
        self.selected = None
        self.answered = False
        self.remaining = seconds_per_question
        self.timer_job = None
        self.frame = tk.Frame(parent, bg=BG)
        self.frame.pack(fill="both", expand=True)
        self._build()
        self._show_question()

    def _build(self):
        header = tk.Frame(self.frame, bg=BG)
        header.pack(fill="x", padx=26, pady=(18, 12))
        tk.Label(header, text="◆  NEON QUIZ", bg=BG, fg=CYAN,
                 font=(FONT, 11, "bold")).pack(side="left")
        self.score_label = tk.Label(header, text="SCORE  0", bg=BG, fg=YELLOW,
                                    font=(FONT, 10, "bold"))
        self.score_label.pack(side="right")

        self.progress_label = tk.Label(self.frame, text="", bg=BG, fg=MUTED,
                                       font=(FONT, 9, "bold"))
        self.progress_label.pack(pady=(0, 8))

        self.progress = tk.Canvas(self.frame, height=5, bg=PANEL_ALT, highlightthickness=0)
        self.progress.pack(fill="x", padx=28, pady=(0, 20))
        self.progress_bar = self.progress.create_rectangle(0, 0, 0, 5, fill=CYAN, width=0)

        self.question_card = tk.Frame(self.frame, bg=PANEL, padx=22, pady=20,
                                      highlightbackground="#263154", highlightthickness=1)
        self.question_card.pack(fill="x", padx=26)
        self.difficulty_label = tk.Label(self.question_card, text="", bg=PANEL, fg=PURPLE,
                                         font=(FONT, 9, "bold"))
        self.difficulty_label.pack(anchor="w", pady=(0, 10))
        self.question_label = tk.Label(self.question_card, text="", bg=PANEL, fg=TEXT,
                                       font=(FONT, 16, "bold"), wraplength=520,
                                       justify="left", anchor="w")
        self.question_label.pack(fill="x")

        timer_row = tk.Frame(self.frame, bg=BG)
        timer_row.pack(fill="x", padx=30, pady=(15, 5))
        tk.Label(timer_row, text="TIME LEFT", bg=BG, fg=MUTED,
                 font=(FONT, 8, "bold")).pack(side="left")
        self.timer_label = tk.Label(timer_row, text="", bg=BG, fg=CYAN,
                                    font=(FONT, 11, "bold"))
        self.timer_label.pack(side="right")

        self.options_frame = tk.Frame(self.frame, bg=BG)
        self.options_frame.pack(fill="both", expand=True, padx=26, pady=8)
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", anchor="w", justify="left",
                            command=lambda choice=i: self._choose(choice),
                            bg=PANEL_ALT, fg=TEXT, activebackground="#26345B",
                            activeforeground=TEXT, relief="flat", bd=0, cursor="hand2",
                            font=(FONT, 10, "bold"), padx=15, pady=11,
                            highlightthickness=1, highlightbackground="#273154")
            btn.pack(fill="x", pady=4)
            self.option_buttons.append(btn)

        self.feedback = tk.Label(self.frame, text="Choose an answer to lock it in.",
                                 bg=BG, fg=MUTED, font=(FONT, 9), wraplength=520)
        self.feedback.pack(padx=24, pady=(2, 8))
        footer = tk.Frame(self.frame, bg=BG)
        footer.pack(fill="x", padx=26, pady=(0, 18))
        self.next_button = tk.Button(footer, text="NEXT QUESTION  →", command=self._next,
                                     bg=CYAN, fg=BG, activebackground="#8AF3FF",
                                     activeforeground=BG, relief="flat", bd=0,
                                     cursor="hand2", font=(FONT, 10, "bold"),
                                     padx=18, pady=10, state="disabled")
        self.next_button.pack(side="right")
        tk.Label(footer, text="Correct answer = 1 point", bg=BG, fg=MUTED,
                 font=(FONT, 8)).pack(side="left")

    def _show_question(self):
        q = self.questions[self.index]
        self.selected = None
        self.answered = False
        self.remaining = self.seconds_per_question
        self.progress_label.config(text=f"QUESTION {self.index + 1:02d}  /  {len(self.questions):02d}")
        self.question_label.config(text=q["question"])
        self.difficulty_label.config(text=f"{q.get('difficulty', 'mixed').upper()} LEVEL")
        self.score_label.config(text=f"SCORE  {self.score}")
        self.feedback.config(text="Choose an answer to lock it in.", fg=MUTED)
        self.next_button.config(state="disabled",
                                text="SEE RESULTS  →" if self.index == len(self.questions)-1 else "NEXT QUESTION  →")
        self.progress.update_idletasks()
        width = max(self.progress.winfo_width(), 200)
        self.progress.coords(self.progress_bar, 0, 0, width * self.index / len(self.questions), 5)
        for i, option in enumerate(q["options"]):
            self.option_buttons[i].config(text=f"  {chr(65+i)}    {option}", state="normal",
                                          bg=PANEL_ALT, fg=TEXT, highlightbackground="#273154")
        self._tick()

    def _tick(self):
        self.timer_label.config(text=f"{self.remaining:02d}s",
                                fg=RED if self.remaining <= 5 else CYAN)
        if self.remaining <= 0:
            self._timeout()
            return
        self.remaining -= 1
        self.timer_job = self.parent.after(1000, self._tick)

    def _cancel_timer(self):
        if self.timer_job is not None:
            try:
                self.parent.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None

    def _choose(self, choice_index):
        if self.answered:
            return
        self._cancel_timer()
        self.answered = True
        self.selected = self.questions[self.index]["options"][choice_index]
        q = self.questions[self.index]
        is_correct = self.selected == q["answer"]
        if is_correct:
            self.score += 1
            self.correct += 1
            self.feedback.config(text=f"✓ Correct! {q.get('explanation', '')}", fg=GREEN)
        else:
            self.wrong += 1
            self.feedback.config(text=f"✕ Not quite. Correct answer: {q['answer']}. {q.get('explanation', '')}", fg=RED)
        self._paint_answer()
        self.score_label.config(text=f"SCORE  {self.score}")
        self.next_button.config(state="normal")
        self.timer_label.config(text="LOCKED", fg=MUTED)

    def _paint_answer(self):
        answer = self.questions[self.index]["answer"]
        for i, option in enumerate(self.questions[self.index]["options"]):
            if option == answer:
                self.option_buttons[i].config(bg="#123C38", fg=GREEN, highlightbackground=GREEN)
            elif option == self.selected:
                self.option_buttons[i].config(bg="#421C32", fg=RED, highlightbackground=RED)
            self.option_buttons[i].config(state="disabled")

    def _timeout(self):
        self._cancel_timer()
        if self.answered:
            return
        self.answered = True
        self.timed_out += 1
        answer = self.questions[self.index]["answer"]
        self.feedback.config(text=f"⌛ Time's up! Correct answer: {answer}", fg=YELLOW)
        for i, option in enumerate(self.questions[self.index]["options"]):
            if option == answer:
                self.option_buttons[i].config(bg="#123C38", fg=GREEN, highlightbackground=GREEN)
            self.option_buttons[i].config(state="disabled")
        self.timer_label.config(text="00s", fg=RED)
        self.next_button.config(state="normal")

    def _next(self):
        self._cancel_timer()
        if not self.answered:
            return
        if self.index + 1 >= len(self.questions):
            self.frame.destroy()
            self.on_finish(self.score, len(self.questions), self.correct, self.wrong, self.timed_out)
            return
        self.index += 1
        self._show_question()

    def destroy(self):
        self._cancel_timer()
        self.frame.destroy()
