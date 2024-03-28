def get_string_score(test_word: str, correct_word: str) -> str:
    length: int = len(correct_word)
    score: list[str] = ["" for _ in range(5)]

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


def find_valid_words(test_word: str, score: str, solutions: set[str]) -> set[str]:
    valid_words = set()
    for word in solutions:
        if get_string_score(test_word, word) == score:
            valid_words.add(word)
    return valid_words


def score_word(test_word: str, correct_word: str) -> int:
    length: int = len(correct_word)
    score: list[int] = [0 for _ in range(5)]

    for i in range(length):
        if test_word[i] == correct_word[i]:
            score[i] = 2

    for i in range(length):
        if score[i] == 0:
            for j in range(length):
                if i == j: continue
                if test_word[i] == correct_word[j]:
                    counter = 0
                    for k in range(length):
                        if correct_word[k] == correct_word[j]: counter += 1
                        if test_word[k] == correct_word[j] and score[k] != 0: counter -= 1
                    if counter > 0: score[i] = 1

    return sum(score)


def scoring_potential(current_word: str, solutions: set[str]) -> int:
    score: int = 0
    for correct_word in solutions:
        if current_word == correct_word: continue
        score += score_word(current_word, correct_word)
    return score


def next_word(guesses: set[str], solutions: set[str]) -> str:
    potentials = {word: scoring_potential(word, solutions) for word in guesses}
    if len(potentials) == 0:
        raise ValueError("No word found!")
    current_word, potential = max(potentials.items(), key=lambda x: x[1])
    return current_word


def guess_word(solutions: set[str]) -> None:
    current_word = "soare"
    solutions.discard(current_word)

    print(f'Current Word: {current_word}')

    for i in range(5):
        score = input("Enter Response: ")
        solutions = find_valid_words(current_word, score, solutions)

        current_word = next_word(solutions, solutions)
        solutions.discard(current_word)

        print(f'Current Word: {current_word}')


def main() -> None:
    with open('solutions.txt', 'r') as f:
        solutions = set([word.strip() for word in f.readlines() if word.strip()])

    guess_word(solutions)


if __name__ == "__main__":
    main()