# UTILS.py
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Codeword generator and solver"
    )

    parser.add_argument(
        "--genGrid",
        action="store_true",
        help="Print the converted grid and exit"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose solver debugging"
    )

    parser.add_argument(
        "--slot",
        type=int,
        help="Inspect a specific slot by ID and exit"
    )

    parser.add_argument(
        "--printSlotGrid",
        action="store_true",
        help="Print a visual grid showing slot start positions and exit"
    )

    parser.add_argument(
        "--slotSummary",
        action="store_true",
        help="Print a summary of all slots and exit"
    )

    parser.add_argument(
        "--prefill",
        action="append",
        help="Prefill a word into a specific slot, e.g. --prefill 12=HELLO"
    )

    parser.add_argument(
        "--printSlotGridV2",
        action="store_true",
        help="Print a visual grid showing slot paths and exit"
    )

    return parser.parse_args()


def print_slot_grid(template, slots):
    """
    Print a visual grid showing slot start positions.
    Across slots are labeled Axx, Down slots Dxx.
    Blocks (#) remain ###.
    """
    h, w = len(template), len(template[0])

    # Prepare empty label grid
    label = [["   " for _ in range(w)] for _ in range(h)]

    # Mark slot starts
    for s in slots:
        tag = f"{s.direction}{s.id:02d}"
        label[s.row][s.col] = tag

    print("\nSlot Grid (slot start positions):")
    for r in range(h):
        row_str = ""
        for c in range(w):
            if template[r][c] == "#":
                row_str += " ###"
            else:
                row_str += f" {label[r][c]}"
        print(row_str)

def print_slot_summary(slots):
    """
    Print a summary of all slots sorted by slot ID.
    Shows: ID, direction, start position, length.
    """
    print("\nSlot Summary (sorted by slot ID):")
    for s in sorted(slots, key=lambda x: x.id):
        print(f"{s.id:2d}: {s.direction}  start=({s.row},{s.col})  len={s.length}")

def inspect_slot(slots, wordlist_by_len, slot_id):
    """Print details and candidate words for a specific slot."""
    slot = next((s for s in slots if s.id == slot_id), None)
    if not slot:
        print(f"No slot with ID {slot_id}")
        return

    print(f"\nSlot {slot.id} details:")
    print(f"  Direction: {slot.direction}")
    print(f"  Start:     ({slot.row}, {slot.col})")
    print(f"  Length:    {slot.length}")
    print(f"  Cells:     {slot.cells}")

    # Candidate words for this slot length
    candidates = wordlist_by_len.get(slot.length, [])
    print(f"\nCandidate words of length {slot.length}: {len(candidates)}")

    # Print a reasonable preview
    for w in candidates[:50]:
        print(" ", w)
    if len(candidates) > 50:
        print("  ...")

def prefill_word(letter_grid, slot, word):
    for (r, c), ch in zip(slot.cells, word):
        letter_grid[r][c] = ch

        
def print_slot_grid_v2(template, slots):
    """
    Visualize slot paths with both Across and Down info preserved.
    - Across: A01→→→
    - Down:   D01 on start, then ↓
    - Overlaps: show both directions, e.g. A01↓ or D18→
    """

    h, w = len(template), len(template[0])

    # Each cell holds a list of symbols (so overlaps don't overwrite)
    grid = [[[] for _ in range(w)] for _ in range(h)]

    # Mark blocks
    for r in range(h):
        for c in range(w):
            if template[r][c] == "#":
                grid[r][c] = ["###"]

    # Draw slot paths
    for s in slots:
        tag = f"{s.direction}{s.id:02d}"

        # Start cell
        r0, c0 = s.row, s.col
        if grid[r0][c0] != ["###"]:
            grid[r0][c0].append(tag)

        # Path cells
        for (r, c) in s.cells[1:]:
            if grid[r][c] == ["###"]:
                continue
            if s.direction == "A":
                grid[r][c].append("→")
            else:
                grid[r][c].append("↓")

    # Print
    print("\nSlot Grid v3 (Across + Down paths):")
    for r in range(h):
        row = ""
        for c in range(w):
            cell = grid[r][c]
            if cell == ["###"]:
                row += " ### "
            elif not cell:
                row += "     "
            else:
                row += f"{''.join(cell):<5}"
        print(row)
