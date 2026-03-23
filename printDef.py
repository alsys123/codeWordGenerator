
# PRINT DEF's

def print_numeric_grid(grid):
    for row in grid:
        print("".join("#" if cell == 1 else "." for cell in row))
