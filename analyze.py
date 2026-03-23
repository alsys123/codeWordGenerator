
#  analyze

from collections import Counter

def count_letter_frequency(letter_grid):
    freq = Counter()
    for row in letter_grid:
        for ch in row:
            if ch not in (None, "#"):
                freq[ch] += 1
    return freq


def pick_hint_letters(letter_grid, mapping, preferred_letters, max_freq=4):
    freq = count_letter_frequency(letter_grid)

    # Step 1: filter to letters that appear AND are in preferred set
    candidates = [
        ch for ch in preferred_letters
        if ch in freq and freq[ch] <= max_freq
    ]

    # If not enough candidates, relax the frequency constraint
    if len(candidates) < 2:
        candidates = [
            ch for ch in preferred_letters
            if ch in freq
        ]

    # Still not enough? fall back to ANY letter with low frequency
    if len(candidates) < 2:
        candidates = [
            ch for ch, f in freq.items()
            if f <= max_freq
        ]

    # Final fallback: any two letters in the puzzle
    if len(candidates) < 2:
        candidates = list(freq.keys())

    # Pick two distinct letters
    if len(candidates) >= 2:
        import random
        chosen = random.sample(candidates, 2)
    else:
        chosen = candidates

    # Convert letters → numbers using mapping
    hints = [{"number": mapping[ch], "letter": ch} for ch in chosen]
    return hints
