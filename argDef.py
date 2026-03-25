
from utils import *

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Codeword generator and solver",
        formatter_class=argparse.RawTextHelpFormatter
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
        help=
           "Prefill a word into a specific slot, e.g. --prefill 12=HELLO \n"
           " or for multi--prefill 12=HELLO --prefill 18=WORLD --prefill 7=RAIN"
    )

    parser.add_argument(
        "--printSlotGridV2",
        action="store_true",
        help="Print a visual grid showing slot paths and exit"
    )

    parser.add_argument(
        "--pickTemplate",
        type=int,
        help="Choose a specific template number instead of random. E.g. 1 .. 7"
    )

    parser.add_argument(
        "--listTemplates",
        action="store_true",
        help="List all available puzzle templates and exit"
    )

    parser.add_argument(
        "--showTemplate",
        type=int,
        help="Display the specified template and exit"
    )

    parser.add_argument(
        "--gen",
        nargs=3,
        metavar=("START", "COUNT", "NAME"),
        help="Generate multiple puzzles: --gen <start> <count> <name>"
    )

    return parser.parse_args()

# argActions.py

def handle_pre_solve_args(args, template, slots, wordlist_by_len):
    if args.printSlotGrid:
        print_slot_grid(template, slots)
        return True

    if args.printSlotGridV2:
        print_slot_grid_v2(template, slots)
        return True

    if args.slot:
        inspect_slot(slots, wordlist_by_len, args.slot)
        return True

    if args.slotSummary:
        print_slot_summary(slots)
        return True

    return False
