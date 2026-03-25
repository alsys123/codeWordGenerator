
# PRINT DEF's

def print_numeric_grid(grid):
    for row in grid:
        print("".join("#" if cell == 1 else "." for cell in row))


import json
import re

def pretty_print_puzzle_json(puzzle_json):
    keys = list(puzzle_json.keys())
    blocks = []

    for key in keys:
        puzzle = puzzle_json[key]
        grid = puzzle["grid"]
        solution = puzzle["solution"]
        hints = puzzle["hints"]

        # -------------------------
        # Format GRID (13 per line)
        # -------------------------
        grid_lines = []
        for i, row in enumerate(grid):
            nums = [str(n) for n in row]
            if len(nums) > 13:
                left = ", ".join(nums[:13])
                right = ", ".join(nums[13:])
                line1 = f"      [ {left},"
                line2 = f"        {right} ]"
                if i < len(grid) - 1:
                    line2 += ","
                grid_lines.append(line1)
                grid_lines.append(line2)
            else:
                line = f"      [ {', '.join(nums)} ]"
                if i < len(grid) - 1:
                    line += ","
                grid_lines.append(line)

        grid_block = "    \"grid\": [\n" + "\n".join(grid_lines) + "\n    ]"

        # -------------------------
        # Format SOLUTION (13 per line)
        # -------------------------
        items = [f"\"{k}\": \"{v}\"" for k, v in solution.items()]
        line1 = ", ".join(items[:13])
        line2 = ", ".join(items[13:])

        solution_block = (
            "    \"solution\": {\n"
            f"      {line1},\n"
            f"      {line2}\n"
            "    }"
        )

        # -------------------------
        # Format HINTS
        # -------------------------
        hint_lines = []
        for h in hints:
            hint_lines.append(
                f"      {{ \"number\": {h['number']}, \"letter\": \"{h['letter']}\" }}"
            )
        hints_block = "    \"hints\": [\n" + ",\n".join(hint_lines) + "\n    ]"

        # -------------------------
        # Assemble this puzzle block
        # -------------------------
        block = (
            f"  \"{key}\": {{\n"
            f"{grid_block},\n"
            f"{solution_block},\n"
            f"{hints_block}\n"
            "  }"
        )

        blocks.append(block)

    # Join all puzzles with commas
    return "{\n" + ",\n".join(blocks) + "\n}"

# def pretty_print_puzzle_json(puzzle_json):
#     key = next(iter(puzzle_json.keys()))
#     puzzle = puzzle_json[key]

#     grid = puzzle["grid"]
#     solution = puzzle["solution"]
#     hints = puzzle["hints"]

#     # # -------------------------
#     # # Format GRID (13 per line)
#     # # -------------------------
#     # grid_lines = []
#     # for row in grid:
#     #     nums = [str(n) for n in row]
#     #     if len(nums) > 13:
#     #         left = ", ".join(nums[:13])
#     #         right = ", ".join(nums[13:])
#     #         grid_lines.append(f"      [ {left},")
#     #         grid_lines.append(f"        {right} ],")
#     #     else:
#     #         grid_lines.append(f"      [ {', '.join(nums)} ],")

#     # grid_block = "    \"grid\": [\n" + "\n".join(grid_lines) + "\n    ]"

#     # -------------------------
#     # Format GRID (13 per line)
#     # -------------------------
#     grid_lines = []
    
#     for i, row in enumerate(grid):
#         nums = [str(n) for n in row]
        
#         if len(nums) > 13:
#             left = ", ".join(nums[:13])
#             right = ", ".join(nums[13:])
#             line1 = f"      [ {left},"
#             line2 = f"        {right} ]"
#             # Add comma only if NOT last row
#             if i < len(grid) - 1:
#                 line2 += ","
#             grid_lines.append(line1)
#             grid_lines.append(line2)
#         else:
#             line = f"      [ {', '.join(nums)} ]"
#             # Add comma only if NOT last row
#             if i < len(grid) - 1:
#                 line += ","
#             grid_lines.append(line)
                    
#     grid_block = "    \"grid\": [\n" + "\n".join(grid_lines) + "\n    ]"
                    
#     # -------------------------
#     # Format SOLUTION (13 per line)
#     # -------------------------
#     items = [f"\"{k}\": \"{v}\"" for k, v in solution.items()]
#     line1 = ", ".join(items[:13])
#     line2 = ", ".join(items[13:])

#     solution_block = (
#         "    \"solution\": {\n"
#         f"      {line1},\n"
#         f"      {line2}\n"
#         "    }"
#     )

#     # -------------------------
#     # Format HINTS (normal JSON)
#     # -------------------------
#     hint_lines = []
#     for h in hints:
#         hint_lines.append(
#             f"      {{ \"number\": {h['number']}, \"letter\": \"{h['letter']}\" }}"
#         )
#     hints_block = "    \"hints\": [\n" + ",\n".join(hint_lines) + "\n    ]"

#     # -------------------------
#     # Assemble final JSON
#     # -------------------------
#     final = (
#         "{\n"
#         f"  \"{key}\": {{\n"
#         f"{grid_block},\n"
#         f"{solution_block},\n"
#         f"{hints_block}\n"
#         "  }\n"
#         "}"
#     )

#     return final

