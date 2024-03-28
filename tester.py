import random
import matplotlib.pyplot as plt
import numpy as np


def find_valid_words(valid_letters: list[set[str]], unknown_letters: list[set[str]], incorrect_letters: list[set[str]], words: set[str]) -> set[str]:
    valid_words: set[str] = set()

    all_unknown_letters = set()
    for letter in unknown_letters:
        all_unknown_letters.update(letter)

    all_valid_letters = set()
    for letter in valid_letters:
        all_valid_letters.update(letter)

    all_incorrect_letters = set()
    for letter in incorrect_letters:
        all_incorrect_letters.update(letter)

    for word in words:
        for i in range(5):
            letter = word[i]
            if letter in incorrect_letters[i]: break
            if letter in unknown_letters[i]: break
            if len(valid_letters[i]) > 0 and letter not in valid_letters[i]: break
        else:
            for letter in all_incorrect_letters:
                if letter in word and letter not in all_valid_letters:
                    break
            else:
                for letter in all_unknown_letters:
                    if letter not in word:
                        break
                else:
                    valid_words.add(word)

    return valid_words


def narrow_wordspace(valid_letters: list[set[str]], unknown_letters: list[set[str]], invalid_letters: list[set[str]], word: str, score: str):
    for i in range(len(word)):
        response = score[i]
        letter = word[i]

        if response == "!":
            invalid_letters[i].add(letter)
        elif response == "?":
            unknown_letters[i].add(letter)
        elif response == "*":
            valid_letters[i].add(letter)

    return valid_letters, unknown_letters, invalid_letters


def get_string_score(test_word: str, correct_word: str) -> str:
    length: int = len(correct_word)
    score = ["" for _ in range(5)]

    for i in range(length):
        if test_word[i] == correct_word[i]:
            score[i] = "*"
        else:
            score[i] = "!"

    for i in range(length):
        if score[i] == "!":
            for j in range(length):
                if i == j: continue
                if test_word[i] == correct_word[j]:
                    counter = 0
                    for k in range(length):
                        if correct_word[k] == correct_word[j]: counter += 1
                        if test_word[k] == correct_word[j] and score[k] != "!": counter -= 1
                    if counter > 0: score[i] = "?"

    return ''.join(score)


def score_word(test_word: str, correct_word: str) -> int:
    score = get_string_score(test_word, correct_word)
    return 2 * score.count("*") + score.count("?")


def scoring_potential(current_word: str, solutions: set[str]) -> int:
    score: int = 0
    for correct_word in solutions:
        if current_word == correct_word: continue
        score += score_word(current_word, correct_word)
    return score


def next_word(guesses: set[str], solutions: set[str]) -> str:
    potentials = {word: scoring_potential(word, solutions) for word in guesses}
    if len(potentials) == 0:
        return ""
        # raise ValueError("No word found!")
    current_word, potential = max(potentials.items(), key=lambda x: x[1])
    return current_word


def guess_word(solutions: set[str], correct_word: str) -> int:
    valid_letters: list[set[str]] = [set() for _ in range(5)]
    unknown_letters: list[set[str]] = [set() for _ in range(5)]
    invalid_letters: list[set[str]] = [set() for _ in range(5)]

    current_word = "soare"
    solutions.discard(current_word)

    for i in range(5):
        if current_word == correct_word:
            return i+1
        score = get_string_score(current_word, correct_word)
        valid_letters, unknown_letters, invalid_letters = narrow_wordspace(valid_letters, unknown_letters, invalid_letters, current_word, score)
        solutions = find_valid_words(valid_letters, unknown_letters, invalid_letters, solutions)

        current_word = next_word(solutions, solutions)
        if not current_word:
            return 0
        solutions.discard(current_word)

    if current_word == correct_word:
        return 6

    return 0

def main() -> None:
    with open('solutions.txt', 'r') as f:
        solutions = [word.strip() for word in f.readlines() if word.strip()]

    values = []
    incorrect = 0
    for i in range(len(solutions)):
        print(f'{i}/{len(solutions)}')
        result = guess_word(set(solutions), solutions[i])
        if result == 0:
            incorrect += 1
            continue
        values.append(result)

    print(f'{incorrect} incorrect guesses')
    print(f'Mean: {np.mean(values)}')
    print(f'Median: {np.median(values)}')
    print(f'Standard Deviation: {np.std(values)}')

    plt.hist(values, bins=np.arange(8)-0.5, ec="k")
    plt.show()

if __name__ == "__main__":
    main()