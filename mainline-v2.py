#!/usr/bin/env python3


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
  [0,0,0,0,0,1,0,0,0,0,0,0,0],
  [0,1,0,1,0,0,0,1,0,1,0,1,0],
  [0,0,0,0,0,0,0,1,0,0,0,0,0],
  [0,1,0,1,0,1,0,1,0,1,0,1,1],
  [0,0,0,1,0,0,0,0,0,0,0,0,0],
  [0,1,0,1,1,1,0,1,0,1,1,1,0],
  [0,0,0,0,0,0,1,0,0,0,0,0,0],
  [0,1,1,1,0,1,0,1,1,1,0,1,0],
  [0,0,0,0,0,0,0,0,1,1,0,0,0],
  [1,1,0,1,0,1,0,0,0,1,0,1,0],
  [0,0,0,0,0,1,0,1,0,0,0,1,0],
  [0,1,0,1,0,1,0,1,0,0,0,0,0],
  [0,0,0,0,0,0,0,1,0,0,0,0,0]
]

#Slot summary:
#  1: A (0,0) len=5
#  2: A (0,6) len=7
#  3: A (1,4) len=3
#  4: A (2,0) len=7
#  5: A (2,8) len=5
#  6: A (4,0) len=3
#  7: A (4,4) len=9
#  8: A (6,0) len=6
#  9: A (6,7) len=6
# 10: A (8,0) len=8
# 11: A (8,10) len=3
# 12: A (9,6) len=3
# 13: A (10,0) len=5
# 14: A (10,8) len=3
# 15: A (11,8) len=5
# 16: A (12,0) len=7
# 17: A (12,8) len=5
# 18: D (0,0) len=9
# 19: D (10,0) len=3
# 20: D (0,2) len=7
# 21: D (8,2) len=5
# 22: D (0,4) len=5
# 23: D (6,4) len=7
# 24: D (1,5) len=2
# 25: D (0,6) len=6
# 26: D (7,6) len=6
# 27: D (8,7) len=2
# 28: D (0,8) len=7
# 29: D (9,8) len=4
# 30: D (10,9) len=3
# 31: D (0,10) len=5
# 32: D (6,10) len=7
# 33: D (11,11) len=2
# 34: D (0,12) len=3
# 35: D (4,12) len=9

def print_slot_grid(template, slots):
    """
    Print a visual grid showing slot IDs.
    Across slots are shown as Axx, Down slots as Dxx.
    Blocks (#) remain #.
    """
    h, w = len(template), len(template[0])

    # Start with blank labels
    label_grid = [["   " for _ in range(w)] for _ in range(h)]

    for s in slots:
        tag = f"{s.direction}{s.id:02d}"  # e.g., A03 or D12
        r, c = s.row, s.col
        label_grid[r][c] = tag

    print("\nSlot Grid (slot start positions):")
    for r in range(h):
        row = ""
        for c in range(w):
            if template[r][c] == "#":
                row += " ###"
            else:
                row += f" {label_grid[r][c]}"
        print(row)

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
        
#    print(f"Try1 slot {idx+1}/{len(slots)} (length {slots[idx].length})")
    if idx == len(slots):
        return assignment

    slot = slots[idx]
    candidates = wordlist_by_len.get(slot.length, [])
    random.shuffle(candidates)

    print(f"Try3 → Slot {idx+1}/{len(slots)}  ID={slot.id}  "
      f"{slot.direction} ({slot.row},{slot.col})  len={slot.length}  "
      f"candidates={len(candidates)}")

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
    print("\nStarting...")
    template = convert_numeric_template(grid)
    
    print("\n")
    print("\nGot template")

    #    template = load_template("grid.txt")
    slots = find_slots(template)

    print("\nSlot summary:")
    for s in slots:
        print(f"{s.id:2d}: {s.direction} ({s.row},{s.col}) len={s.length}")
        #    print("\nFound Slots")
        
    wordlist_by_len = load_wordlist("words.txt")
        
    slots.sort(key=lambda s: len(wordlist_by_len.get(s.length, [])))

    print("\nLoaded word list")
    letter_grid = init_letter_grid(template)

    print_slot_grid(template, slots)
    
    print("\nInitialized letter grid.")
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
                
                
if __name__ == "__main__":
    main()
                    
                    
                    
