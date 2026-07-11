import random

HIRAGANA_DATA = {
    # Vowels
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    # K-Row
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    # S-Row
    "さ": "sa", "し": "shi", "す": "su", "ぜ": "se", "そ": "so",
    # T-Row
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    # N-Row
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no"
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
    "ナ": "na", "ニ": "ni", "ヌ": "nu", "ネ": "ne", "ノ": "no"
}

def run_quiz():
    print("Welcome to your Japanese Learning MVP!")
    
    # 1. Ask the user for their preferred mode
    print("Choose what you want to practice:")
    print("1. Hiragana")
    print("2. Katakana")
    choice = input("Enter 1 or 2: ").strip()
    
    # 2. Select the data dictionary dynamically based on choice
    if choice == "2":
        quiz_data = KATAKANA_DATA
        print("\nStarting Katakana Quiz!")
    else:
        quiz_data = HIRAGANA_DATA
        print("\nStarting Hiragana Quiz!")
        
    print("Type the correct English sound for the character. Type 'q' to quit.\n")

    # 3. Use quiz_data to get the characters
    characters = list(quiz_data.keys())

    while True:
        # Pick a random character from our selected list
        char = random.choice(characters)
        correct_answer = quiz_data[char]

        user_guess = input(f"What is the sound for '{char}'? ").strip().lower()

        if user_guess == 'q':
            print("\nJa mata ne! (See you later!) Thanks for practicing.")
            break
        elif user_guess == correct_answer:
            print("Correct! Excellent job.\n")
        else:
            print(f"Oops! The correct sound was '{correct_answer}'.\n")

if __name__ == "__main__":
    run_quiz()
