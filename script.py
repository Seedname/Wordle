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


def score_word(test_word: str, correct_word: str) -> int:
    score: int = 0
    possible_letters = {}

    for i in range(len(test_word)):
        test_letter = test_word[i]
        correct_letter = correct_word[i]
        if test_letter == correct_letter:
            score += 2
        elif test_letter in correct_word:
            if not possible_letters.get(test_letter):
                possible_letters[test_letter] = 0
            possible_letters[test_letter] += 1

    for letter in test_word:
        if possible_letters.get(letter):
            possible_letters[letter] -= 1
            if possible_letters[letter] >= 0:
                score += 1

    return score


def get_string_score(test_word: str, correct_word: str) -> str:
    score = ["" for _ in range(5)]
    possible_letters = {}

    for i in range(len(test_word)):
        test_letter = test_word[i]
        correct_letter = correct_word[i]
        if test_letter == correct_letter:
            score[i] = '*'
        elif test_letter not in correct_word:
            score[i] = "!"
        elif test_letter in correct_word:
            if not possible_letters.get(test_letter):
                possible_letters[test_letter] = 0
            possible_letters[test_letter] += 1

    for i in range(len(test_word)):
        if score[i] == "":
            letter = test_word[i]
            possible_letters[letter] -= 1
            if possible_letters[letter] >= 0:
                score[i] = "?"
            else:
                score[i] = "!"

    return ''.join(score)

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


def guess_word(guesses: set[str], solutions: set[str]) -> None:
    valid_letters: list[set[str]] = [set() for _ in range(5)]
    unknown_letters: list[set[str]] = [set() for _ in range(5)]
    invalid_letters: list[set[str]] = [set() for _ in range(5)]

    current_word = "saree"
    guesses.discard(current_word)
    solutions.discard(current_word)

    print(f'Current Word: {current_word}')

    for i in range(5):
        score = input("Enter Response: ")
        valid_letters, unknown_letters, invalid_letters = narrow_wordspace(valid_letters, unknown_letters, invalid_letters, current_word, score)
        solutions = find_valid_words(valid_letters, unknown_letters, invalid_letters, solutions)

        if score.count("*") >= 3 or i >= 1 or len(solutions) == 1:
            guesses = solutions.copy()

        current_word = next_word(guesses, solutions)
        guesses.discard(current_word)
        solutions.discard(current_word)

        print(f'Current Word: {current_word}')

def main() -> None:
    with open('guesses.txt', 'r') as f:
        guesses = set([word.strip() for word in f.readlines() if word.strip()])

    with open('solutions.txt', 'r') as f:
        solutions = set([word.strip() for word in f.readlines() if word.strip()])

    guess_word(guesses, solutions)


if __name__ == "__main__":
    main()