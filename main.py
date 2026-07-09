import random

# A mini dictionary matching Hiragana characters to their English sounds (Romaji)
HIRAGANA_MVP = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o"
}

def run_quiz():
    print("🇯🇵 Welcome to your Japanese Learning MVP! 🇯🇵")
    print("Type the correct English sound for the character. Type 'q' to quit.\n")
    
    characters = list(HIRAGANA_MVP.keys())
    
    while True:
        # Pick a random character from our list
        char = random.choice(characters)
        correct_answer = HIRAGANA_MVP[char]
        
        user_guess = input(f"What is the sound for '{char}'? ").strip().lower()
        
        if user_guess == 'q':
            print("\n👋 Ja mata ne! (See you later!) Thanks for practicing.")
            break
        elif user_guess == correct_answer:
            print("✅ Correct! Excellent job.\n")
        else:
            print(f"❌ Oops! The correct sound was '{correct_answer}'.\n")

if __name__ == "__main__":
    run_quiz()
