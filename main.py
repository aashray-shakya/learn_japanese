import random

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
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no"
}

def run_quiz():
    print(" Welcome to your Japanese Learning MVP!")
    print("Type the correct English sound for the character. Type 'q' to quit.\n")
    
    characters = list(HIRAGANA_DATA.keys())
    
    while True:
        # Pick a random character from our list
        char = random.choice(characters)
        correct_answer = HIRAGANA_DATA[char]
        
        user_guess = input(f"What is the sound for '{char}'? ").strip().lower()
        
        if user_guess == 'q':
            print("\n Ja mata ne! (See you later!) Thanks for practicing.")
            break
        elif user_guess == correct_answer:
            print(" Correct! Excellent job.\n")
        else:
            print(f" Oops! The correct sound was '{correct_answer}'.\n")

if __name__ == "__main__":
    run_quiz()
