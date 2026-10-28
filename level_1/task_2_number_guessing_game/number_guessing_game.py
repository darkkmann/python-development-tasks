"""A command-line number guessing game."""
from __future__ import annotations

import random


def evaluate_guess(guess: int, target: int) -> str:
    """Return feedback for a valid guess."""
    if guess < target:
        return "Too low."
    if guess > target:
        return "Too high."
    return "Correct!"


def play(max_attempts: int = 7, lower: int = 1, upper: int = 100) -> None:
    target = random.randint(lower, upper)
    print(f"Guess a number between {lower} and {upper}. You have {max_attempts} attempts.")
    for attempt in range(1, max_attempts + 1):
        try:
            guess = int(input(f"Attempt {attempt}/{max_attempts}: "))
        except ValueError:
            print("Please enter a whole number.")
            continue
        if not lower <= guess <= upper:
            print(f"Enter a number from {lower} to {upper}.")
            continue
        feedback = evaluate_guess(guess, target)
        print(feedback)
        if guess == target:
            print(f"You won in {attempt} attempt(s)!")
            return
    print(f"Out of {attempt} attempts. The number was {target}.")


if __name__ == "__main__":
    play()
