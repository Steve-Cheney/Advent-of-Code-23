"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""
import sys

def isSymbol(char):
    return (not char.isdigit()) and (char != ".") and (char != "\n")

def getNums(line):
    # key: starting index
    # value: (ending index, num)
    numDict = {}
    i = 0
    while i < (len(line) - 1):
        if line[i].isdigit():
            startindex = i
            digstr = line[i]
            count = 1
            i += 1
            while line[i].isdigit() and i < len(line) - 1:
                digstr += line[i]
                count += 1
                i += 1
            numDict[startindex] = (i - 1, digstr)
        i += 1
    return numDict

def file_to_matrix(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read lines from the file
            lines = file.readlines()

            # Create a 2D matrix
            matrix = [list(line.strip()) for line in lines]

            return matrix

    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
        return None

def getAllNums(file):
    f = open(file, "r")
    allNums = []
    for line in f.readlines():
        allNums.append(getNums(line))
    return allNums

def isValidNum(matrix, line_index, start_index, end_index):
    rows, cols = len(matrix), len(matrix[0])

    top_line = matrix[line_index - 1] if line_index > 0 else None
    current_line = matrix[line_index]
    bottom_line = matrix[line_index + 1] if line_index < rows - 1 else None

    surrounding_indices = []

    # Top line
    if top_line is not None:
        surrounding_indices.extend([(line_index - 1, i) for i in range(max(0, start_index - 1), min(cols, end_index + 2))])

    # Same line
    # Keep indices to the left and right, but not within the start and end range
    surrounding_indices.extend([(line_index, i) for i in range(max(0, start_index - 1), min(cols, end_index + 2))
                                if i <= start_index - 1 or (i >= end_index + 1 and i < cols)])
    # Bottom line
    if bottom_line is not None:
        surrounding_indices.extend([(line_index + 1, i) for i in range(max(0, start_index - 1), min(cols, end_index + 2))])

    # Filter out invalid indices
    surrounding_indices = [(i, j) for i, j in surrounding_indices if 0 <= i < rows and 0 <= j < cols]

    for ind_pair in surrounding_indices:
        if isSymbol(matrix[ind_pair[0]][ind_pair[1]]):
            return True
    return False

def part1(file):
    allNums = getAllNums(file)
    matrix = file_to_matrix(file)
    result_list = []
    for i, num in enumerate(allNums):
        #print(i)
        #print(allSymbs[i])
        #print(allNums[i])
        for numStart in num:
            start = numStart
            end = num[numStart][0]
            if isValidNum(matrix, i, start, end):
                result_list.append(int(num[numStart][1]))
    return sum(result_list)



if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Please provide only the input file")
        sys.exit(1)
    file = sys.argv[1]
    output = part1(file)
    print("Part 1 sum:", output)
    #output2 = part2(file)
    #print("Part 2 sum:", output2)