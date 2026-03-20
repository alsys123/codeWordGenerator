#!/usr/bin/env python3

#from utils import print_slot_grid, print_slot_summary,inspect_slot
from utils import *

# or import utils ... and use like utils.print_slot_summary
import argDef  

##..#...#...#..
#...#...#...#..
#...#...#...#..
##..#...#...#..
#...#...#...#..
#...#...#...#..
##..#...#...#..
#...#...#...#..
#...#...#...#..
##..#...#...#..
#...#...#...#..
#...#...#...#..
##..#...#...#..
grid = [
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
]

# grid = [
#   [0,0,0,0,0,1,0,0,0,0,0,0,0],
#   [0,1,0,1,0,0,0,1,0,1,0,1,0],
#   [0,0,0,0,0,0,0,1,0,0,0,0,0],
#   [0,1,0,1,0,1,0,1,0,1,0,1,1],
#   [0,0,0,1,0,0,0,0,0,0,0,0,0],
#   [0,1,0,1,1,1,0,1,0,1,1,1,0],
#   [0,0,0,0,0,0,1,0,0,0,0,0,0],
#   [0,1,1,1,0,1,0,1,1,1,0,1,0],
#   [0,0,0,0,0,0,0,0,1,1,0,0,0],
#   [1,1,0,1,0,1,0,0,0,1,0,1,0],
#   [0,0,0,0,0,1,0,1,0,0,0,1,0],
#   [0,1,0,1,0,1,0,1,0,0,0,0,0],
#   [0,0,0,0,0,0,0,1,0,0,0,0,0]
# ]

RARE_LETTERS = set("JQXZKVWY")

def convert_numeric_template(num_grid):
    return [
        ['#' if cell == 1 else '.' for cell in row]
        for row in num_grid
    ]

def load_template(path: str):
    grid = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            row = [c for c in line.strip()]
            if row:
                grid.append(row)
    return grid  # list[list[str]]

from dataclasses import dataclass

@dataclass
class Slot:
    id: int
    direction: str  # "A" or "D"
    row: int
    col: int
    length: int
    cells: list[tuple[int, int]]  # (r, c)

def find_slots(grid):
    h, w = len(grid), len(grid[0])
    slots = []
    slot_id = 1

    # Across
    for r in range(h):
        c = 0
        while c < w:
            while c < w and grid[r][c] == '#':
                c += 1
            start = c
            while c < w and grid[r][c] != '#':
                c += 1
            length = c - start
            if length >= 2:
                cells = [(r, cc) for cc in range(start, c)]
                slots.append(Slot(slot_id, "A", r, start, length, cells))
                slot_id += 1

    # Down
    for c in range(w):
        r = 0
        while r < h:
            while r < h and grid[r][c] == '#':
                r += 1
            start = r
            while r < h and grid[r][c] != '#':
                r += 1
            length = r - start
            if length >= 2:
                cells = [(rr, c) for rr in range(start, r)]
                slots.append(Slot(slot_id, "D", start, c, length, cells))
                slot_id += 1

    return slots

from collections import defaultdict

def load_wordlist(path: str):
    by_len = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip().upper()
            if w.isalpha():
                by_len[len(w)].append(w)
    return by_len  # dict[length] -> list[str]

import random

def init_letter_grid(template):
    h, w = len(template), len(template[0])
    g = []
    for r in range(h):
        row = []
        for c in range(w):
            if template[r][c] == '#':
                row.append('#')
            else:
                row.append(None)
        g.append(row)
    return g

def fits(word, slot, letter_grid):
    for (i, (r, c)) in enumerate(slot.cells):
        ch = letter_grid[r][c]
        if ch is not None and ch != word[i]:
            return False
    return True

# def place(word, slot, letter_grid):
#     for (i, (r, c)) in enumerate(slot.cells):
#         letter_grid[r][c] = word[i]

# def unplace(word, slot, letter_grid):
#     for (i, (r, c)) in enumerate(slot.cells):
#         # Only clear if this cell is not forced by another slot.
#         # Simple version: just set to None and rely on backtracking.
#         # For a robust engine, track reference counts per cell.
#         letter_grid[r][c] = None
def place(word, slot, letter_grid):
    """
    Place a word into the grid, but only record cells that were empty.
    """
    filled = []  # cells this slot actually filled

    for i, (r, c) in enumerate(slot.cells):
        if letter_grid[r][c] is None:
            letter_grid[r][c] = word[i]
            filled.append((r, c))

    # store which cells we filled so unplace() can undo safely
    slot.filled_cells = filled

def unplace(word, slot, letter_grid):
    """
    Remove only the letters that this slot placed.
    """
    for (r, c) in slot.filled_cells:
        letter_grid[r][c] = None

    slot.filled_cells = []
    
# Def solve(slots, wordlist_by_len, letter_grid, idx=0, assignment=None):
#     if assignment is None:
#         assignment = {}

#     # Base case: all slots filled
#     if idx == len(slots):
#         return assignment

#     slot = slots[idx]
#     print(f"\n=== Try slotIndex {idx+1}/{len(slots)} → slotID={slot.id} length={slot.length} ===")
#     #    print_partial_grid(letter_grid)

#     # Get candidates
#     #candidates = wordlist_by_len.get(slot.length, [])
    
#     candidates = get_candidates_for_slot(slot, letter_grid, wordlist_by_len)
#     #
#     random.shuffle(candidates)
    
#     for w in candidates:
#         # Skip if this word is already used in another slot
#         if w in assignment.values():
#             continue
    
#         if fits(w, slot, letter_grid):
#             print(f"Placing {w} into slot {slot.id}")
#             place(w, slot, letter_grid)
#             print_partial_grid(letter_grid)

#             assignment[slot.id] = w
            
#             res = solve(slots, wordlist_by_len, letter_grid, idx + 1, assignment )
#             if res is not None:
#                 return res

#             print(f"Backtracking {w} from slot {slot.id}")
#             unplace(w, slot, letter_grid)
#             print_partial_grid(letter_grid)

#             del assignment[slot.id]

#     return None

# def get_candidates_for_slot(slot, letter_grid, wordlist_by_len):
#     pattern = []
#     r, c = slot.row, slot.col
#     for i in range(slot.length):
#         ch = letter_grid[r][c]
#         pattern.append(ch if ch else ".")
#         if slot.direction == "A":
#             c += 1
#         else:
#             r += 1

#     pat = "".join(pattern)

#     return [
#         w for w in wordlist_by_len[slot.length]
#         if all(p == "." or p == w[i] for i, p in enumerate(pat))
#     ]

## NEW
def pattern_for_slot(slot, letter_grid):
    """Return pattern string like 'A..E.' for this slot."""
    chars = []
    r, c = slot.row, slot.col
    for _ in range(slot.length):
        ch = letter_grid[r][c]
        chars.append(ch if ch else ".")
        if slot.direction == "A":
            c += 1
        else:
            r += 1
    return "".join(chars)


def candidates_for_slot(slot, letter_grid, wordlist_by_len):
    """Filter wordlist by length and pattern."""
    all_words = wordlist_by_len.get(slot.length, [])
    pat = pattern_for_slot(slot, letter_grid)
    return [
        w for w in all_words
        if all(p == "." or p == w[i] for i, p in enumerate(pat))
    ]


def forward_check(slots, letter_grid, wordlist_by_len, assignment):
    """Ensure every unfilled slot still has at least one candidate."""
    for s in slots:
        if s.id in assignment:
            continue
        cand = candidates_for_slot(s, letter_grid, wordlist_by_len)
        if not cand:
            return False
    return True


def choose_next_slot(slots, letter_grid, wordlist_by_len, assignment):
    """Dynamic MRV: choose the unfilled slot with the fewest candidates."""
    best = None
    best_count = None

    for s in slots:
        if s.id in assignment:
            continue

        cand = candidates_for_slot(s, letter_grid, wordlist_by_len)
        cnt = len(cand)

        if cnt == 0:
            return None  # immediate dead end

        if best is None or cnt < best_count:
            best = s
            best_count = cnt

    return best

def get_used_letters(letter_grid):
    return {
        ch for row in letter_grid for ch in row
        if ch not in (None, "#")
    }

def solve(slots, wordlist_by_len, letter_grid, assignment=None, depth=0):
    if assignment is None:
        assignment = {}

    # All slots filled
#    if len(assignment) == len(slots):
#        return assignment

    if len(assignment) == len(slots):
    # Final constraint: must use all 26 letters
        if puzzle_uses_all_letters(letter_grid):
            return assignment
        else:
            # Reject this solution and force backtracking
            return None

    # Pick next slot dynamically (MRV)
    slot = choose_next_slot(slots, letter_grid, wordlist_by_len, assignment)
    if slot is None:
        return None

    # Get filtered candidates
    candidates = candidates_for_slot(slot, letter_grid, wordlist_by_len)

    # ---------------------------------------------------------
    # RARE LETTER HEURISTIC (conditional, keeps randomness)
    # ---------------------------------------------------------
    
    used = get_used_letters(letter_grid)
    missing_rare = RARE_LETTERS - used
    
    progress = len(assignment) / len(slots)
    
    # Activate heuristic only after 40% of puzzle is filled
    if progress > 0.40 and missing_rare:
        # Filter candidates that contain ANY missing rare letter
        filtered = [w for w in candidates if set(w) & missing_rare]
        
        if filtered:
            # Keep randomness but bias toward rare-letter words
            random.shuffle(filtered)
            candidates = filtered
        else:
            # No rare-letter words available — keep original list
            random.shuffle(candidates)
    else:
        # Early in puzzle: pure randomness
        random.shuffle(candidates)

    # end of RARE letter
        
    print(f"\n{'  '*depth}=== SlotID {slot.id} len={slot.length} "
          f"candidates={len(candidates)} ===")

    for w in candidates:
        # Enforce uniqueness
        if w in assignment.values():
            continue

        if not fits(w, slot, letter_grid):
            continue

        print(f"{'  '*depth}Placing {w} into slot {slot.id}")
        place(w, slot, letter_grid)
        assignment[slot.id] = w
        print_partial_grid(letter_grid)

        # Forward checking
        if forward_check(slots, letter_grid, wordlist_by_len, assignment):
            res = solve(slots, wordlist_by_len, letter_grid, assignment, depth+1)
            if res is not None:
                return res

        # Backtrack
        print(f"{'  '*depth}Backtracking {w} from slot {slot.id}")
        unplace(w, slot, letter_grid)
        del assignment[slot.id]
        print_partial_grid(letter_grid)

    return None


## end of new

def build_letter_number_mapping(letter_grid):
    letters = sorted({ch for row in letter_grid for ch in row if ch not in (None, '#')})
    # You can randomize or use a fixed mapping
    random.shuffle(letters)
    mapping = {}
    num = 1
    for ch in letters:
        mapping[ch] = num
        num += 1
    return mapping  # dict[letter] -> number

def encode_grid(letter_grid, mapping):
    h, w = len(letter_grid), len(letter_grid[0])
    encoded = []
    for r in range(h):
        row = []
        for c in range(w):
            ch = letter_grid[r][c]
            if ch == '#':
                row.append('#')
            else:
                row.append(str(mapping[ch]))
        encoded.append(row)
    return encoded


def print_js_puzzle(puzzle_id, letter_grid, mapping, hints=None):
    print(f"  {puzzle_id}: {{")
    print("    grid: [")

    # Convert letter grid → numeric grid
    encoded = encoded_grid_2(letter_grid, mapping)

    # Print grid rows
    for row in encoded:
        nums = []
        for x in row:
            if x == "#" or x is None:
                nums.append("0")
            else:
                nums.append(str(int(x)))
        print(f"      [ {', '.join(nums)} ],")

    print("    ],\n")

    # Print solution block
    print("    solution: {")
    inv = {v: k for k, v in mapping.items()}  # number → letter
    for num in range(1, 27):
        letter = inv.get(num, "?")
        print(f"      {num}:\"{letter}\",")
    print("    },\n")

    # Print hints block
    print("    hints: [")
    if hints:
        for h in hints:
            print(f"      {{ number: {h['number']}, letter: \"{h['letter']}\" }},")
    print("    ]")

    print("  },")

def encoded_grid_2(letter_grid, mapping):
    encoded = []
    for row in letter_grid:
        out_row = []
        for ch in row:
            if ch is None or ch == "#":
                out_row.append(0)
            else:
                out_row.append(mapping[ch])
        encoded.append(out_row)
    return encoded

def puzzle_uses_all_letters(letter_grid):
    letters = {ch for row in letter_grid for ch in row if ch not in (None, "#")}
    return len(letters) == 26

def main():
    args = argDef.parse_args()

    print("\nStarting...")

    template = convert_numeric_template(grid)

    if args.genGrid:
        print("\nConverted grid:")
        for row in template:
            print("".join(row))
        return

    slots = find_slots(template)

    wordlist_by_len = load_wordlist("words.txt")

    # MRV sort
    slots.sort(key=lambda s: len(wordlist_by_len.get(s.length, [])))

    # Handle all early-exit argument actions
    if argDef.handle_pre_solve_args(args, template, slots, wordlist_by_len):
        return
    
    if args.debug:
        print("\nSlot summary:")
        for s in slots:
            print(f"{s.id:2d}: {s.direction} ({s.row},{s.col}) len={s.length}")
            
    letter_grid = init_letter_grid(template)

    # ⭐ PREFILL GOES HERE ⭐
    if args.prefill:
        for item in args.prefill:
            slot_id, word = item.split("=")
            slot_id = int(slot_id)
            slot = next(s for s in slots if s.id == slot_id)
            prefill_word(letter_grid, slot, word.upper())

# # ⭐⭐⭐ INSERT RETRY LOOP HERE ⭐⭐⭐
#     print("\nSolving...")

#     while True:
#         # fresh grid each attempt
#         letter_grid = init_letter_grid(template)

#         # apply prefill again if needed
#         if args.prefill:
#             for item in args.prefill:
#                 slot_id, word = item.split("=")
#                 slot_id = int(slot_id)
#                 slot = next(s for s in slots if s.id == slot_id)
#                 prefill_word(letter_grid, slot, word.upper())

#         solution = solve(slots, wordlist_by_len, letter_grid)

#         if solution is None:
#             print("No fill found — retrying...\n")
#             continue

#         if puzzle_uses_all_letters(letter_grid):
#             print("Puzzle uses all 26 letters — accepted.")
#             break

#         print("Puzzle missing letters — retrying...\n")
# # ⭐⭐⭐ END RETRY LOOP ⭐⭐⭐

    print("\nSolving...")
    solution = solve(slots, wordlist_by_len, letter_grid)

    print("\nSolve Complete.")

    if solution is None:
        print("No fill found.")
        return

    mapping = build_letter_number_mapping(letter_grid)
    encoded = encode_grid(letter_grid, mapping)

    print("Solved letter grid:")
    for row in letter_grid:
        print("".join(ch if ch is not None else "." for ch in row))

    print("\nCodeword grid (numbers):")
    for row in encoded:
        print(" ".join(row))

    print("\nLetter→number mapping:")
    for ch, num in sorted(mapping.items(), key=lambda x: x[1]):
        print(f"{num:2d}: {ch}")

    print("\nJS Puzzle Output:\n")
    print_js_puzzle(
        1,
        letter_grid,
        mapping,
        hints=[{"number":5,"letter":"Q"}, {"number":23,"letter":"Z"}]
    )

                
if __name__ == "__main__":
    main()
                    
                    
                    
