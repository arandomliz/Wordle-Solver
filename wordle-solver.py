from typing import Set
from collections import Counter
from random import choice
import re


wordle_list_file = "wordle-answers-alphabetical.txt"

with open(wordle_list_file, "r") as f:
    words = f.read().splitlines()


class AnswerException(Exception):
    ...


def w_filter(pos: str, included: Set, excluded: Set) -> Set:
    """ Filter word list by possible candidates according to previous answers """
    included = (set(pos) | included) - {'*'}
    excluded = excluded - included  # can happen due to how wordle highlights

    f_words = filter(lambda w: excluded.isdisjoint(set(w)), words)
    f_words = filter(lambda w: included.issubset(set(w)), f_words)
    f_words = filter(
        lambda w: all(map(lambda t: t[0] == "*" or t[0] == t[1], zip(pos, w))),
        f_words
    )

    return list(f_words)


def get_optimal_word(word_list: Set) -> str:
    """ get most optimal word from word list
    Heuristic based on letter frequency, no repeating letters, …
    """

    # letter frequency score
    letter_count = Counter()
    for word in words:
        letter_count.update(word)

    frequency_score = {
        word: 1 / sum(map(letter_count.get, word))
        for word in word_list
    }

    # prever words with no repeating letters
    unique_score = {
        word: len(word) - len(set(word))
        for word in word_list
    }

    # scoring
    score = {w: unique_score[w] + frequency_score[w] for w in word_list}

    min_value = min(score.values())
    possible_values = list(filter(lambda w: score[w] == min_value, score))
    print(f" - possible {len(possible_values)}")
    return possible_values[0]


def terminal():
    excluded = set()
    included = set()
    position = "*****"

    def get_guess():
        guesses = w_filter(position, included, excluded)
        guess = get_optimal_word(guesses)
        return len(guesses), guess

    l_guesses, guess = get_guess()

    while True:
        answer = input(f"Guessing '{guess}' ({l_guesses}) > ")

        if answer != "":
            try:
                pos, inc = map(lambda w: w.lower().strip(), answer.split(","))
            except ValueError:
                pos = answer.lower().strip()
                inc = ""
        else:
            pos, inc = ("", "")

        if pos.strip() == "":
            pos = position

        try:  # processing
            if not re.fullmatch(r"[a-z\*]{5}", pos):
                raise AnswerException("Invalid position input")

            # merge positions
            new_pos = list("*****")
            for i, (f1, f2) in enumerate(zip(position, pos)):
                if f1 != f2 and f1 != "*" and f2 != "*":
                    raise AnswerException("Would overwrite known positions")
                if guess[i] != f2 and f2 != "*":
                    raise AnswerException("Position argument doesn't match guess")

                new_pos[i] = f2 if f1 == "*" else f1

            # parse inclusion
            if not re.fullmatch(r"[a-z]*", inc):
                raise AnswerException("Invalid included input")
            if len(diff := set(inc) - set(guess)) > 0:
                raise AnswerException(f"Letter(s) {diff} weren't included in guess")

            # write new values
            position = "".join(new_pos)
            included |= set(inc) | (set(new_pos) - {'*'})
            excluded |= set(guess) - included
        except AnswerException as e:
            print(f"invalid input: {e}")
            continue

        l_guesses, guess = get_guess()
        print("------------------")


if __name__ == "__main__":
    terminal()
