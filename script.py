from collections import Counter


def get_string_score(test_word: str, correct_word: str) -> str:
    score = ['!' for _ in range(5)]
    correct_counter = Counter(correct_word)

    # First pass: mark exact matches
    for i, (t, c) in enumerate(zip(test_word, correct_word)):
        if t == c:
            score[i] = '*'
            correct_counter[c] -= 1

    # Second pass: mark partial matches
    for i, (t, s) in enumerate(zip(test_word, score)):
        if s == '!' and t in correct_counter and correct_counter[t] > 0:
            score[i] = '?'
            correct_counter[t] -= 1

    return ''.join(score)


def find_valid_words(test_word: str, score: str, solutions: set[str]) -> set[str]:
    return {word for word in solutions if get_string_score(test_word, word) == score}


def score_word(test_word: str, correct_word: str) -> int:
    score = get_string_score(test_word, correct_word)
    return sum(2 if c == '*' else 1 if c == '?' else 0 for c in score)


def scoring_potential(current_word: str, solutions: set[str]) -> int:
    return sum(score_word(current_word, word) for word in solutions if current_word != word)


def next_word(guesses: set[str], solutions: set[str]) -> str:
    return max(guesses, key=lambda word: scoring_potential(word, solutions))


def guess_word(solutions: set[str]) -> None:
    current_word = input("Enter word or leave blank to auto-generate: ") or "soare"

    for i in range(5):
        print(f'Current Word: {current_word}')
        score = input("Enter Response: ")

        if score == "*****":
            print("Solved!")
            break

        solutions = find_valid_words(current_word, score, solutions)
        solutions.discard(current_word)

        current_word = input("Enter word or leave blank to auto-generate: ") or next_word(solutions, solutions)


def main() -> None:
    with open('solutions.txt', 'r') as f:
        solutions = {word.strip() for word in f if word.strip()}

    guess_word(solutions)


if __name__ == "__main__":
    main()
