"""
--- Day 8: Haunted Wasteland ---
You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""
import sys

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __str__(self):
        return self.val

def parseFile(file):
    f = open(file, "r")
    lines = f.readlines()
    instructions = lines[0]
    nodes = []
    for line in lines[2:]:
        strlist = [char for char in line if char.isalpha()]
        strlist = ["".join(strlist[i:i+3]) for i in range(0, len(strlist), 3)]
        nodes.append((strlist[0], strlist[1], strlist[2]))
    nodes = sorted(nodes, key = lambda x:x[0])
    
    node_dict = {}
    root = None
    for value, left, right in nodes:
        current_node = node_dict.get(value, Node(value))
        node_dict[value] = current_node

        if left:
            left_node = node_dict.get(left, Node(left))
            current_node.left = left_node
            node_dict[left] = left_node

        if right:
            right_node = node_dict.get(right, Node(right))
            current_node.right = right_node
            node_dict[right] = right_node

        if not root:
            root = current_node

    return instructions, root


def part1(file):

    instructions, root = parseFile(file)
    instructions = ''.join(instructions.split('\n'))
    steps = 0
    index = 0
    curr = root
    while True:
        if curr.val == 'ZZZ':
            return steps
        if index == len(instructions):
            index = 0
        direc = instructions[index]
        
        if direc == 'L':
            curr = curr.left
            steps += 1
            index += 1
        elif direc == 'R':
            curr = curr.right
            steps += 1
            index += 1


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Please provide only the input file")
        sys.exit(1)
    file = sys.argv[1]
    output = part1(file)
    print("Part 1 answer:", output)
    #output2 = part2(file)
    #print("Part 2 answer:", output2)