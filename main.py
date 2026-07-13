import random
import tkinter as tk
from tkinter import font as tkfont

HIRAGANA_DATA = {
    # Vowels
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    # K-Row
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    # S-Row
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    # T-Row
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    # N-Row
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
}

KATAKANA_DATA = {
    # Vowels
    "ア": "a", "イ": "i", "ウ": "u", "エ": "e", "オ": "o",
    # K-Row
    "カ": "ka", "キ": "ki", "ク": "ku", "ケ": "ke", "コ": "ko",
    # S-Row
    "サ": "sa", "シ": "shi", "ス": "su", "セ": "se", "ソ": "so",
    # T-Row
    "タ": "ta", "チ": "chi", "ツ": "tsu", "テ": "te", "ト": "to",
    # N-Row
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no",
}

# ---- Minimal color palette ----
BG = "#fafafa"
FG = "#1a1a1a"
MUTED = "#8a8a8a"
ACCENT = "#2563eb"
CORRECT = "#16a34a"
WRONG = "#dc2626"
ENTRY_BG = "#ffffff"
BORDER = "#e0e0e0"


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Japanese Quiz")
        self.geometry("420x480")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.char_font = tkfont.Font(family="Helvetica", size=64)
        self.label_font = tkfont.Font(family="Helvetica", size=13)
        self.feedback_font = tkfont.Font(family="Helvetica", size=12)
        self.score_font = tkfont.Font(family="Helvetica", size=11)

        self.quiz_data = HIRAGANA_DATA
        self.current_char = ""
        self.correct_answer = ""
        self.score = 0
        self.total = 0
        self.remaining = []

        self._build_mode_screen()

    # ---------- Screen 1: choose mode ----------
    def _build_mode_screen(self):
        self.mode_frame = tk.Frame(self, bg=BG)
        self.mode_frame.pack(expand=True, fill="both")

        tk.Label(
            self.mode_frame, text="Japanese Quiz", font=("Helvetica", 22, "bold"),
            bg=BG, fg=FG
        ).pack(pady=(80, 10))

        tk.Label(
            self.mode_frame, text="Choose what you'd like to practice",
            font=self.label_font, bg=BG, fg=MUTED
        ).pack(pady=(0, 30))

        tk.Button(
            self.mode_frame, text="Hiragana", font=self.label_font,
            bg=ACCENT, fg="white", activebackground="#1d4ed8", activeforeground="white",
            relief="flat", width=18, height=2, cursor="hand2",
            command=lambda: self.start_quiz(HIRAGANA_DATA)
        ).pack(pady=6)

        tk.Button(
            self.mode_frame, text="Katakana", font=self.label_font,
            bg="white", fg=ACCENT, activebackground="#f0f0f0",
            relief="flat", width=18, height=2, cursor="hand2",
            highlightbackground=BORDER, highlightthickness=1,
            command=lambda: self.start_quiz(KATAKANA_DATA)
        ).pack(pady=6)

    # ---------- Screen 2: quiz ----------
    def start_quiz(self, data):
        self.quiz_data = data
        self.score = 0
        self.total = 0
        self.remaining = list(data.keys())
        random.shuffle(self.remaining)
        self.mode_frame.destroy()
        self._build_quiz_screen()
        self.next_question()

    def _build_quiz_screen(self):
        self.quiz_frame = tk.Frame(self, bg=BG)
        self.quiz_frame.pack(expand=True, fill="both")

        top_bar = tk.Frame(self.quiz_frame, bg=BG)
        top_bar.pack(fill="x", padx=20, pady=(20, 0))

        self.score_label = tk.Label(
            top_bar, text="Score: 0 / 0", font=self.score_font, bg=BG, fg=MUTED
        )
        self.score_label.pack(side="left")

        tk.Button(
            top_bar, text="Quit", font=self.score_font, bg=BG, fg=MUTED,
            relief="flat", cursor="hand2", command=self.destroy
        ).pack(side="right")

        self.char_label = tk.Label(
            self.quiz_frame, text="", font=self.char_font, bg=BG, fg=FG
        )
        self.char_label.pack(pady=(50, 10))

        tk.Label(
            self.quiz_frame, text="What's the sound?", font=self.label_font,
            bg=BG, fg=MUTED
        ).pack(pady=(0, 20))

        self.answer_var = tk.StringVar()
        self.entry = tk.Entry(
            self.quiz_frame, textvariable=self.answer_var, font=("Helvetica", 16),
            justify="center", bg=ENTRY_BG, fg=FG, relief="flat",
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT
        )
        self.entry.pack(ipady=8, padx=60, fill="x")
        self.entry.bind("<Return>", self.check_answer)
        self.entry.focus_set()

        self.feedback_label = tk.Label(
            self.quiz_frame, text="", font=self.feedback_font, bg=BG, fg=MUTED
        )
        self.feedback_label.pack(pady=20)

        tk.Button(
            self.quiz_frame, text="Submit", font=self.label_font,
            bg=ACCENT, fg="white", activebackground="#1d4ed8", activeforeground="white",
            relief="flat", width=16, height=1, cursor="hand2",
            command=self.check_answer
        ).pack(pady=10)

    def next_question(self):
        if not self.remaining:
            self.show_completed_screen()
            return
        self.current_char = random.choice(self.remaining)
        self.correct_answer = self.quiz_data[self.current_char]
        self.char_label.config(text=self.current_char)
        self.answer_var.set("")
        self.entry.focus_set()

    def check_answer(self, event=None):
        guess = self.answer_var.get().strip().lower()
        if not guess:
            return
        self.total += 1
        if guess == self.correct_answer:
            self.score += 1
            self.remaining.remove(self.current_char)
            self.feedback_label.config(text="Correct! Excellent job.", fg=CORRECT)
        else:
            self.feedback_label.config(
                text=f"Oops! The correct sound was '{self.correct_answer}'.", fg=WRONG
            )
        self.score_label.config(text=f"Score: {self.score} / {self.total}")
        self.after(900, self.next_question)

    # ---------- Screen 3: completed ----------
    def show_completed_screen(self):
        self.quiz_frame.destroy()
        self.done_frame = tk.Frame(self, bg=BG)
        self.done_frame.pack(expand=True, fill="both")

        tk.Label(
            self.done_frame, text="All done!", font=("Helvetica", 22, "bold"),
            bg=BG, fg=FG
        ).pack(pady=(90, 10))

        tk.Label(
            self.done_frame, text=f"You cleared every character.\nFinal score: {self.score} / {self.total}",
            font=self.label_font, bg=BG, fg=MUTED, justify="center"
        ).pack(pady=(0, 30))

        tk.Button(
            self.done_frame, text="Play Again", font=self.label_font,
            bg=ACCENT, fg="white", activebackground="#1d4ed8", activeforeground="white",
            relief="flat", width=18, height=2, cursor="hand2",
            command=self.restart
        ).pack(pady=6)

        tk.Button(
            self.done_frame, text="Quit", font=self.label_font,
            bg="white", fg=MUTED, activebackground="#f0f0f0",
            relief="flat", width=18, height=2, cursor="hand2",
            highlightbackground=BORDER, highlightthickness=1,
            command=self.destroy
        ).pack(pady=6)

    def restart(self):
        self.done_frame.destroy()
        self._build_mode_screen()


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
