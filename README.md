# Learn Japanese

A desktop flashcard/quiz app for practicing Japanese kana (hiragana & katakana), built with Python and Tkinter.

## What it does

- Quizzes you on hiragana or katakana characters, one at a time
- Tracks your score and shows a progress bar as you clear the character pool
- Auto-detects an installed Japanese-capable font, so characters render cleanly wherever possible
- Currently covers vowels through the N-row (あ–の / ア–ノ) — more rows (H, M, Y, R, W, and dakuten) coming later

## Setup

Requires Python 3 with Tkinter.

Tkinter usually ships with Python by default, but on some Linux distros you may need to install it separately:

```bash
sudo apt install python3-tk
```

For crisp Japanese character rendering, it also helps to have a CJK-capable font installed:

```bash
sudo apt install fonts-noto-cjk
```

If no Japanese font is found, the app still runs — it just prints a notice and characters may look a bit blocky.

## Usage

```bash
python3 main.py
```

Pick Hiragana or Katakana from the start screen, then type the romanized sound for each character and hit Enter (or click Submit).

## Notes

- Vocabulary is currently hardcoded in `main.py` — could be extended to load from an external file (JSON/CSV) for easier editing
- Built and run from the Linux terminal

