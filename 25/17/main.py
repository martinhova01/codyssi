import time
import itertools
import functools
from collections import Counter, defaultdict, deque
import networkx as nx
from tqdm import tqdm
import numpy as np
import re
import copy
from functools import cache
import matplotlib.pyplot as plt

import sys
sys.path.append("../..")
from utils import adjacent4, adjacent8, directions4, directions8, manhattanDist

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        self.parse()
        
    def parse(self):
        stairs, possible_moves = self.data.split("\n\n")
        self.stairs = {}
        self.G = nx.DiGraph()
        for line in stairs.split("\n"):
            stair, steps, branch = line.split(" : ")
            steps = tuple(map(int, steps.split(" -> ")))
            self.stairs[stair] = steps
            for step in range(*steps):
                self.G.add_edge((stair, step), (stair, step + 1))
                
            if "START" in branch:
                continue
            _from, to = tuple(re.findall(r"S\d+", branch))
            print(_from, to)
            self.G.add_edge((_from, steps[0]), (stair, steps[0]))
            self.G.add_edge((stair, steps[1]), (to, steps[1]))

        self.possible_moves = tuple(map(int, re.findall(r"\d+", possible_moves)))
    
    @cache
    def paths(self, _from, to, possible_moves):
        if _from == to:
            return 1
        s = 0
        for move in possible_moves:
            if _from + move <= to:
                s += self.paths(_from + move, to, possible_moves)
        return s
    

    def bfs_layers(self, source):
        q = deque([(source, 0)])
        res = defaultdict(list)
        while q:
            node, dept = q.popleft()
            res[dept].append(node)
            for next_node in self.G.successors(node):
                q.append((next_node, dept + 1))
        return res
    
    
    @cache
    def paths_2(self, node):
        if node == ("S1", self.stairs["S1"][1]):
            return 1
        
        next_nodes = set()
        for layer, nodes in self.bfs_layers(node).items():
            if layer not in self.possible_moves:
                continue
            next_nodes.update(nodes)
        
        s = 0
        for next_node in next_nodes:
            s += self.paths_2(next_node)
        return s
        
        
    def part1(self):
        return self.paths(*self.stairs["S1"], self.possible_moves)
    
    def part2(self):
        return self.paths_2(("S1", 0))
        
    
    def part3(self):
        return None
    
    
def main():
    start = time.perf_counter()
    
    s = Solution(test=True)
    print("---TEST---")
    print(f"part 1: {s.part1()}")
    part2 = s.part2()
    assert part2 == 113524314072255566781694 
    print(f"part 2: {part2}")
    print(f"part 3: {s.part3()}\n")
    
    s = Solution()
    print("---MAIN---")
    print(f"part 1: {s.part1()}")
    part2 = s.part2()
    assert part2 != 115790115638940139516655311982964
    assert part2 != 113632294802551734246135778434644
    print(f"part 2: {part2}")
    print(f"part 3: {s.part3()}")
    
    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    
main()