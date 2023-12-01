"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ('not powerful enough') and where they're even sending you ('the sky') and why your map looks mostly blank ('you sure ask a lot of questions') and hang on did you just say the sky ('of course, where do you think snow comes from') when you realize that the Elves are already loading you into a trebuchet ('please hold still, we need to strap you in').

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
"""
import sys
import re

def part1(file):
    f = open(file, "r")
    number_extract_pattern = "\\d+"
    sum = 0
    for line in f.readlines():
        nums = re.findall(number_extract_pattern, line) # returns ['203']
        numStr = ''.join(nums)
        strList = [*numStr]
        num = int(strList[0] + strList[-1])
        sum += num
    return sum

NUM_DICT = {
    'one':'1',
    'two':'2',
    'three':'3',
    'four':'4',
    'five':'5',
    'six':'6',
    'seven':'7',
    'eight':'8',
    'nine':'9'
}    



def part2(file):
    @staticmethod
    def find_starting_indices(input_string, num_dict):
        result_dict = {}
        
        for key, value in num_dict.items():
            indices = [i for i in range(len(input_string)) if input_string.startswith(key, i)]
            for index in indices:
                result_dict[index] = value
        
        return result_dict

    f = open(file, "r")
    sum = 0
    for line in f.readlines():
        int_dict = {}
        for i, char in enumerate(line):
            if char.isdigit():
                int_dict[i] = char
        
        str_dict = find_starting_indices(line, NUM_DICT)
        int_dict.update(str_dict)

        sorted_keys = sorted(int_dict.keys())
        first_key = sorted_keys[0]
        last_key = sorted_keys[-1]
        
        num = int(int_dict[first_key] + int_dict[last_key])
        sum += num
    return sum

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Please provide only the input file")
        sys.exit(1)
    file = sys.argv[1]
    output = part1(file)
    print("Part 1 sum:", output)
    output2 = part2(file)
    print("Part 2 sum:", output2)