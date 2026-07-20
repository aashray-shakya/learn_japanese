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

# ---- Color palette ----
BG = "#f7f7f5"
CARD = "#ffffff"
FG = "#1a1a1a"
MUTED = "#9a9a95"
ACCENT = "#3b5bdb"
ACCENT_HOVER = "#2f4bc4"
ACCENT_SOFT = "#eef1fd"
CORRECT = "#2f9e44"
WRONG = "#e03131"
ENTRY_BG = "#ffffff"
BORDER = "#e7e7e3"
TRACK = "#eeeeeb"


def find_japanese_font():
    """Pick the best available font that can render Japanese glyphs cleanly."""
    candidates = [
        "Noto Sans CJK JP", "Noto Sans JP", "Noto Serif CJK JP",
        "Source Han Sans JP", "Source Han Sans", "IPAexGothic", "IPAexMincho",
        "Hiragino Sans", "Hiragino Kaku Gothic Pro",
        "Yu Gothic", "Meiryo", "MS Gothic",
        "TakaoPGothic", "IPAGothic", "IPAPGothic", "VL Gothic", "Sazanami Gothic",
        "Droid Sans Fallback", "WenQuanYi Zen Hei", "WenQuanYi Micro Hei",
        "AR PL UMing CN", "AR PL UKai CN", "Unifont",
    ]
    available = list(tkfont.families())
    available_set = set(available)
    for name in candidates:
        if name in available_set:
            return name

    # Fuzzy fallback: scan every installed font for CJK-ish keywords
    keywords = ["cjk", "noto sans", "gothic", "mincho", "han sans", "unifont", "fallback"]
    for name in available:
        lowered = name.lower()
        if any(k in lowered for k in keywords):
            return name

    return None  # nothing found — caller should warn the user


def add_hover(widget, normal_bg, hover_bg):
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
    widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Japanese Quiz")
        self.geometry("440x560")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        jp_font_name = find_japanese_font()
        self.jp_font_available = jp_font_name is not None
        self.char_font = tkfont.Font(family=jp_font_name or "Helvetica", size=68)
        self.label_font = tkfont.Font(family="Helvetica", size=13)
        self.small_font = tkfont.Font(family="Helvetica", size=11)
        self.feedback_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        if not self.jp_font_available:
            print(
                "\n[Notice] No Japanese font detected on this system, so characters "
                "may render blocky/pixelated.\nInstall one for crisp text, e.g. on "
                "Debian/Ubuntu:\n    sudo apt install fonts-noto-cjk\nthen re-run the app.\n"
            )

        self.quiz_data = HIRAGANA_DATA
        self.current_char = ""
        self.correct_answer = ""
        self.score = 0
        self.total = 0
        self.remaining = []
        self.pool_size = 0

        self._build_mode_screen()

    # ---------- Screen 1: choose mode ----------
    def _build_mode_screen(self):
        self.mode_frame = tk.Frame(self, bg=BG)
        self.mode_frame.pack(expand=True, fill="both")

        tk.Label(
            self.mode_frame, text="ひ / カ", font=("Helvetica", 30),
            bg=BG, fg=ACCENT
        ).pack(pady=(90, 6))

        tk.Label(
            self.mode_frame, text="Japanese Quiz", font=self.title_font,
            bg=BG, fg=FG
        ).pack(pady=(0, 6))

        tk.Label(
            self.mode_frame, text="Choose what you'd like to practice",
            font=self.label_font, bg=BG, fg=MUTED
        ).pack(pady=(0, 36) if self.jp_font_available else (0, 12))

        if not self.jp_font_available:
            tk.Label(
                self.mode_frame,
                text="Tip: install a Japanese font for crisper text\n(e.g. sudo apt install fonts-noto-cjk)",
                font=self.small_font, bg=BG, fg=WRONG, justify="center"
            ).pack(pady=(0, 24))

        hira_btn = tk.Button(
            self.mode_frame, text="Hiragana", font=self.label_font,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            relief="flat", bd=0, width=20, height=2, cursor="hand2",
            command=lambda: self.start_quiz(HIRAGANA_DATA)
        )
        hira_btn.pack(pady=6)
        add_hover(hira_btn, ACCENT, ACCENT_HOVER)

        kata_btn = tk.Button(
            self.mode_frame, text="Katakana", font=self.label_font,
            bg=CARD, fg=ACCENT, activebackground=ACCENT_SOFT, activeforeground=ACCENT,
            relief="flat", bd=0, width=20, height=2, cursor="hand2",
            highlightbackground=BORDER, highlightthickness=1,
            command=lambda: self.start_quiz(KATAKANA_DATA)
        )
        kata_btn.pack(pady=6)
        add_hover(kata_btn, CARD, ACCENT_SOFT)

    # ---------- Screen 2: quiz ----------
    def start_quiz(self, data):
        self.quiz_data = data
        self.score = 0
        self.total = 0
        self.remaining = list(data.keys())
        self.pool_size = len(self.remaining)
        random.shuffle(self.remaining)
        self.mode_frame.destroy()
        self._build_quiz_screen()
        self.next_question()

    def _build_quiz_screen(self):
        self.quiz_frame = tk.Frame(self, bg=BG)
        self.quiz_frame.pack(expand=True, fill="both")

        # ---- top bar ----
        top_bar = tk.Frame(self.quiz_frame, bg=BG)
        top_bar.pack(fill="x", padx=24, pady=(22, 0))

        self.score_label = tk.Label(
            top_bar, text="Score: 0 / 0", font=self.small_font, bg=BG, fg=MUTED
        )
        self.score_label.pack(side="left")

        quit_btn = tk.Button(
            top_bar, text="Quit", font=self.small_font, bg=BG, fg=MUTED,
            relief="flat", bd=0, cursor="hand2", command=self.destroy
        )
        quit_btn.pack(side="right")
        add_hover(quit_btn, BG, TRACK)

        # ---- progress bar ----
        progress_wrap = tk.Frame(self.quiz_frame, bg=BG)
        progress_wrap.pack(fill="x", padx=24, pady=(14, 0))

        self.progress_track = tk.Frame(progress_wrap, bg=TRACK, height=6)
        self.progress_track.pack(fill="x")
        self.progress_fill = tk.Frame(self.progress_track, bg=ACCENT, height=6, width=0)
        self.progress_fill.place(x=0, y=0, relheight=1)

        self.progress_label = tk.Label(
            progress_wrap, text="", font=self.small_font, bg=BG, fg=MUTED
        )
        self.progress_label.pack(anchor="w", pady=(6, 0))

        # ---- card ----
        card = tk.Frame(
            self.quiz_frame, bg=CARD, highlightbackground=BORDER,
            highlightthickness=1
        )
        card.pack(padx=24, pady=24, fill="both", expand=True)

        self.char_label = tk.Label(
            card, text="", font=self.char_font, bg=CARD, fg=FG
        )
        self.char_label.pack(pady=(46, 8))

        tk.Label(
            card, text="What's the sound?", font=self.label_font,
            bg=CARD, fg=MUTED
        ).pack(pady=(0, 22))

        self.answer_var = tk.StringVar()
        self.entry = tk.Entry(
            card, textvariable=self.answer_var, font=("Helvetica", 17),
            justify="center", bg=ENTRY_BG, fg=FG, relief="flat",
            highlightthickness=1.5, highlightbackground=BORDER, highlightcolor=ACCENT,
            insertbackground=FG
        )
        self.entry.pack(ipady=10, padx=50, fill="x")
        self.entry.bind("<Return>", self.check_answer)
        self.entry.bind("<KeyRelease>", self._reset_entry_color)
        self.entry.focus_set()

        self.feedback_label = tk.Label(
            card, text=" ", font=self.feedback_font, bg=CARD, fg=MUTED
        )
        self.feedback_label.pack(pady=(18, 4))

        submit_btn = tk.Button(
            card, text="Submit", font=self.label_font,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            relief="flat", bd=0, width=18, height=1, cursor="hand2",
            command=self.check_answer
        )
        submit_btn.pack(pady=(10, 40), ipady=6)
        add_hover(submit_btn, ACCENT, ACCENT_HOVER)

    def _reset_entry_color(self, event=None):
        self.entry.config(highlightbackground=BORDER, highlightcolor=ACCENT)

    def _update_progress(self):
        done = self.pool_size - len(self.remaining)
        frac = done / self.pool_size if self.pool_size else 0
        track_width = self.progress_track.winfo_width() or 392
        self.progress_fill.place(width=max(2, int(track_width * frac)))
        self.progress_label.config(
            text=f"{done} / {self.pool_size} characters mastered"
        )

    def next_question(self):
        if not self.remaining:
            self.show_completed_screen()
            return
        self.current_char = random.choice(self.remaining)
        self.correct_answer = self.quiz_data[self.current_char]
        self.char_label.config(text=self.current_char)
        self.answer_var.set("")
        self.feedback_label.config(text=" ", fg=MUTED)
        self.after(10, self._update_progress)
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
            self.entry.config(highlightbackground=CORRECT, highlightcolor=CORRECT)
        else:
            self.feedback_label.config(
                text=f"Oops! The correct sound was '{self.correct_answer}'.", fg=WRONG
            )
            self.entry.config(highlightbackground=WRONG, highlightcolor=WRONG)
        self.score_label.config(text=f"Score: {self.score} / {self.total}")
        self.after(900, self.next_question)

    # ---------- Screen 3: completed ----------
    def show_completed_screen(self):
        self.quiz_frame.destroy()
        self.done_frame = tk.Frame(self, bg=BG)
        self.done_frame.pack(expand=True, fill="both")

        tk.Label(
            self.done_frame, text="🎉", font=("Helvetica", 40),
            bg=BG, fg=FG
        ).pack(pady=(100, 10))

        tk.Label(
            self.done_frame, text="All done!", font=self.title_font,
            bg=BG, fg=FG
        ).pack(pady=(0, 8))

        accuracy = round((self.score / self.total) * 100) if self.total else 0
        tk.Label(
            self.done_frame,
            text=f"You cleared every character.\nFinal score: {self.score} / {self.total}  ({accuracy}% accuracy)",
            font=self.label_font, bg=BG, fg=MUTED, justify="center"
        ).pack(pady=(0, 34))

        again_btn = tk.Button(
            self.done_frame, text="Play Again", font=self.label_font,
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            relief="flat", bd=0, width=20, height=2, cursor="hand2",
            command=self.restart
        )
        again_btn.pack(pady=6)
        add_hover(again_btn, ACCENT, ACCENT_HOVER)

        quit_btn = tk.Button(
            self.done_frame, text="Quit", font=self.label_font,
            bg=CARD, fg=MUTED, activebackground=TRACK, activeforeground=MUTED,
            relief="flat", bd=0, width=20, height=2, cursor="hand2",
            highlightbackground=BORDER, highlightthickness=1,
            command=self.destroy
        )
        quit_btn.pack(pady=6)
        add_hover(quit_btn, CARD, TRACK)

    def restart(self):
        self.done_frame.destroy()
        self._build_mode_screen()


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
