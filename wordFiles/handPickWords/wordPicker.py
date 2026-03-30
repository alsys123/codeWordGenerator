#!/usr/bin/env python3

import os
import argparse

# Utility: load a file into a set (fast lookup)
def load_word_set(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

# Utility: load a file into a list (preserves order)
def load_word_list(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Utility: append a word to a file
def append_word(filename, word):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(word + "\n")

def classify_words(source_file, files):
    words = load_word_set(files["w"])
    rejected = load_word_set(files["r"])
    notsure = load_word_set(files["n"])

    with open(source_file, "r", encoding="utf-8") as f:
        all_words = [line.strip() for line in f if line.strip()]

    for word in all_words:
        if word in words or word in rejected or word in notsure:
            continue  # Already classified

        print(f"\nWord: {word}")
        print("Where should this go?")
        print("  [w] words.txt")
        print("  [r] rejectedWords.txt")
        print("  [n] notSureWords.txt")
        print("  [s] skip")
        print("  [x] exit program")

        while True:
            choice = input("Choice: ").strip().lower()
            if choice in ("w", "r", "n"):
                append_word(files[choice], word)
                break
            elif choice == "s":
                break
            elif choice == "x":
                print("Exiting.")
                exit(0)
            else:
                print("Invalid choice. Use w/r/n/s/x.")

def review_rejected(files):
    rejected_list = load_word_list(files["r"])
    if not rejected_list:
        print("No rejected words to review.")
        return

    print(f"\nReviewing {len(rejected_list)} rejected words:")

    for word in rejected_list:
        print(f"\nRejected word: {word}")
        print("Move it to:")
        print("  [w] words.txt")
        print("  [n] notSureWords.txt")
        print("  [s] skip (keep rejected)")
        print("  [x] exit program")

        while True:
            choice = input("Choice: ").strip().lower()
            if choice == "w":
                append_word(files["w"], word)
                break
            elif choice == "n":
                append_word(files["n"], word)
                break
            elif choice == "s":
                break
            elif choice == "x":
                print("Exiting.")
                exit(0)
            else:
                print("Invalid choice. Use w/n/s/x.")

def review_not_sure(files):
    notsure_list = load_word_list(files["n"])
    if not notsure_list:
        print("No not-sure words to review.")
        return

    print(f"\nReviewing {len(notsure_list)} not-sure words:")

    for word in notsure_list:
        print(f"\nNot-sure word: {word}")
        print("Move it to:")
        print("  [w] words.txt")
        print("  [r] rejectedWords.txt")
        print("  [s] skip (keep in not-sure)")
        print("  [x] exit program")


        while True:
            choice = input("Choice: ").strip().lower()
            if choice == "w":
                append_word(files["w"], word)
                break
            elif choice == "r":
                append_word(files["r"], word)
                break
            elif choice == "s":
                break
            elif choice == "x":
                print("Exiting.")
                exit(0)
            else:
                print("Invalid choice. Use w/r/s/x.")

def main():
    parser = argparse.ArgumentParser(description="Word classification tool")

    parser.add_argument("--new", "-n", action="store_true",
                        help="Process completeWordFile.txt (default behavior)")

    parser.add_argument("--rejected", action="store_true",
                        help="Review rejectedWords.txt interactively")

    parser.add_argument("--not-sure", action="store_true",
                        help="Review notSureWords.txt interactively")
    
    args = parser.parse_args()

    files = {
        "w": "words.txt",
        "r": "rejectedWords.txt",
        "n": "notSureWords.txt"
    }

    if args.rejected:
        review_rejected(files)
    elif args.not_sure:
        review_not_sure(files)
    else:
        # default or --new
        classify_words("completeWordFile.txt", files)

    print("\nDone.")

if __name__ == "__main__":
    main()
