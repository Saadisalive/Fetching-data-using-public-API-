import requests
import html
import random
from colorama import Fore

EDUCATION_CATEGORY_ID = 9
API_URL = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def get_education_questions():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if data['response_code'] == 0 and data['results']:
            return data['results']
    return None

def run_quiz():
    questions = get_education_questions()
    if not questions:
        print(Fore.RED + "Failed to fetch questions.")
        return

    score = 0
    print(Fore.CYAN + "Welcome to the Education Quiz!")

    for i, q in enumerate(questions, 1):
        question = html.unescape(q['question'])
        correct = html.unescape(q['correct_answer'])
        incorrects = [html.unescape(a) for a in q['incorrect_answers']]

        options = incorrects + [correct]
        random.shuffle(options)

        print(f"\n{Fore.CYAN}Question {i}: {question}")
        for idx, option in enumerate(options, 1):
            print(f"  {Fore.YELLOW}{idx}. {option}")

        while True:
            try:
                choice = int(input(Fore.RESET + "Your answer (1-4): "))
                if 1 <= choice <= 4:
                    break
                else:
                    print(Fore.MAGENTA + "Please enter a number between 1 and 4.")
            except ValueError:
                print(Fore.MAGENTA + "Invalid input. Please enter a number between 1 and 4.")

        if options[choice - 1] == correct:
            print(Fore.GREEN + "Correct!")
            score += 1
        else:
            print(Fore.RED + f"Wrong! " + Fore.GREEN + f"The correct answer was: {correct}")

    print(Fore.MAGENTA + f"\nFinal Score: {score} / {len(questions)}")
    print(Fore.MAGENTA + f"Percentage: {score / len(questions) * 100:.1f}%")

if __name__ == "__main__":
    run_quiz()