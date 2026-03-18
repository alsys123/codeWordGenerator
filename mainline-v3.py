#!/usr/bin/env python3

#from utils import print_slot_grid, print_slot_summary,inspect_slot
from utils import *
# or import utils ... and use like utils.print_slot_summary

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

def place(word, slot, letter_grid):
    for (i, (r, c)) in enumerate(slot.cells):
        letter_grid[r][c] = word[i]

def unplace(word, slot, letter_grid):
    for (i, (r, c)) in enumerate(slot.cells):
        # Only clear if this cell is not forced by another slot.
        # Simple version: just set to None and rely on backtracking.
        # For a robust engine, track reference counts per cell.
        letter_grid[r][c] = None

def solve(slots, wordlist_by_len, letter_grid, idx=0, assignment=None):
    if assignment is None:
        assignment = {}
        
    print(f"Try1 slot {idx+1}/{len(slots)} (length {slots[idx].length})")
    if idx == len(slots):
        return assignment

    slot = slots[idx]
    candidates = wordlist_by_len.get(slot.length, [])
    random.shuffle(candidates)

#    print(f"Try3 → Slot {idx+1}/{len(slots)}  ID={slot.id}  "
#      f"{slot.direction} ({slot.row},{slot.col})  len={slot.length}  "
#      f"candidates={len(candidates)}")

    for w in candidates:
#        print(f"   Try2 {w} for slot {slot.id}")
        if fits(w, slot, letter_grid):
            place(w, slot, letter_grid)
            assignment[slot.id] = w
            res = solve(slots, wordlist_by_len, letter_grid, idx + 1, assignment)
            if res is not None:
                return res
            unplace(w, slot, letter_grid)
            del assignment[slot.id]

    return None

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


def main():
    args = parse_args()

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

    # Handle --printSlotGrid
    if args.printSlotGrid:
        print_slot_grid(template, slots)
        return

    if args.printSlotGridV2:
        print_slot_grid_v2(template, slots)
        return

    # Handle --slot N
    if args.slot:
        inspect_slot(slots, wordlist_by_len, args.slot)
        return

    if args.debug:
        print("\nSlot summary:")
        for s in slots:
            print(f"{s.id:2d}: {s.direction} ({s.row},{s.col}) len={s.length}")

    if args.slotSummary:
        print_slot_summary(slots)
        return
            
    letter_grid = init_letter_grid(template)

    # ⭐ PREFILL GOES HERE ⭐
    if args.prefill:
        for item in args.prefill:
            slot_id, word = item.split("=")
            slot_id = int(slot_id)
            slot = next(s for s in slots if s.id == slot_id)
            prefill_word(letter_grid, slot, word.upper())
            
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

# def main():
#     print("\nStarting...")
#     template = convert_numeric_template(grid)
    
#     print("\n")
#     print("\nGot template")

#     #    template = load_template("grid.txt")
#     slots = find_slots(template)

#     print("\nSlot summary:")
#     for s in slots:
#         print(f"{s.id:2d}: {s.direction} ({s.row},{s.col}) len={s.length}")
#         #    print("\nFound Slots")
        
#     wordlist_by_len = load_wordlist("words.txt")
        
#     slots.sort(key=lambda s: len(wordlist_by_len.get(s.length, [])))

#     print("\nLoaded word list")
#     letter_grid = init_letter_grid(template)

#     print_slot_grid(template, slots)
    
#     print("\nInitialized letter grid.")
#     print("\nSolving...")
#     solution = solve(slots, wordlist_by_len, letter_grid)

#     print("\nSolve Complete.")

#     if solution is None:
#         print("No fill found.")
#         return
    
#     mapping = build_letter_number_mapping(letter_grid)
#     encoded = encode_grid(letter_grid, mapping)
    
#     print("Solved letter grid:")
#     for row in letter_grid:
#         print("".join(ch if ch is not None else "." for ch in row))
        
#     print("\nCodeword grid (numbers):")
#     for row in encoded:
#         print(" ".join(row))
            
#     print("\nLetter→number mapping:")
#     for ch, num in sorted(mapping.items(), key=lambda x: x[1]):
#         print(f"{num:2d}: {ch}")
                
                
if __name__ == "__main__":
    main()
                    
                    
                    
