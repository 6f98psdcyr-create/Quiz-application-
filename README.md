# Neon Quiz Application (Python + Tkinter)

A desktop multiple-choice quiz game with a neon gaming theme, a per-question countdown timer, answer feedback, scoring, a result screen, and replay functionality.

## Requirements

- Python 3.9 or newer
- Tkinter (included with most standard Python installations)
- No third-party Python packages required

## Project files

```text
QuizApplication/
├── main.py
├── quiz.py
├── results.py
├── styles.py
├── questions.json
└── README.md
```

## Run it

1. Extract the project ZIP.
2. Open a terminal in the `QuizApplication` folder.
3. Check Python:

   ```bash
   python --version
   ```

4. Start the game:

   ```bash
   python main.py
   ```

On some Linux distributions, if Tkinter is missing, install it with your package manager, for example `sudo apt install python3-tk`. On Windows, use the official Python installer and ensure Tcl/Tk support is selected.

## Game rules

- Each round selects 10 questions randomly from `questions.json`.
- Each question has four answer options and a 15-second timer.
- Correct answer: +1 point.
- Incorrect answer or timeout: 0 points.
- Maximum score: 10 points.
- Score percentage: `score / total_questions * 100`.
- After choosing an answer, the game locks the options and shows feedback. Press **Next Question** to continue.
- If time runs out, the question is marked as timed out and the correct answer is revealed.
- The result screen reports score, percentage, correct answers, incorrect answers, and timeouts.
- **Play Again** starts a fresh round with a newly randomized question selection.

## Customize

- Change `QUESTION_COUNT` and `SECONDS_PER_QUESTION` in `main.py`.
- Add questions to `questions.json`. Each question must have:
  - `question`: question text
  - `options`: exactly four unique or distinct choices
  - `answer`: exact text of one option
  - `difficulty`: optional label
  - `explanation`: optional explanation shown after answering

Example:

```json
{
  "question": "What is 3 + 4?",
  "options": ["5", "6", "7", "8"],
  "answer": "7",
  "difficulty": "easy",
  "explanation": "Three plus four equals seven."
}
```

## Troubleshooting

- **`No module named tkinter`**: install the Tk/Tcl component for your Python installation. On Ubuntu/Debian, run `sudo apt install python3-tk`.
- **Question file error**: keep `questions.json` in the same directory and launch the app from that directory.
- **Timer seems too fast**: the timer uses Tkinter's event loop and `after(1000, ...)`; avoid long-running blocking code in UI callbacks.
