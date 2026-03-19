
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

    return parser.parse_args()
