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
        self.branches = defaultdict(list)
        for line in stairs.split("\n"):
            stair, steps, branch = line.split(" : ")
            self.stairs[stair] = tuple(map(int, steps.split(" -> ")))
            if "START" in branch:
                continue
            _from, to = tuple(re.findall(r"S\d+", branch))
            self.branches[_from].append((stair, self.stairs[stair][0]))
            self.branches[stair].append((to, self.stairs[stair][1]))

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


    @cache
    def paths_2(self, staircase, step):
        # print(staircase, step)
        top = self.stairs[staircase][1]
        if step == top and staircase == "S1":
            return 1
        
        s = 0
        for move in self.possible_moves:
            
            
            q = deque()
            for branch, branch_step in self.branches[staircase]:
                q.append((branch, branch_step, step, move))
            
            while q:
                
                branch, branch_step, current_step, moves_left = q.popleft()
                
                #cannot reach branch
                if branch_step not in range(current_step, current_step + moves_left):
                    continue
                # print(branch, branch_step, current_step, moves_left)
                    
                if current_step + moves_left - 1 <= self.stairs[branch][1]:
                    if (staircase, step, branch, current_step + moves_left - 1) not in self.moves_done:
                        s += self.paths_2(branch, current_step + moves_left - 1)
                        self.moves_done.add((staircase, step, branch, current_step + moves_left - 1))
                    
                steps_to_branch = branch_step - step
                if steps_to_branch + 1 < moves_left:
                    moves_left -= (steps_to_branch + 1)
                    for next_branch, next_branch_step in self.branches[branch]:
                        q.append((next_branch, next_branch_step, branch_step, moves_left))
                        
                        
                        
                
            if step + move <= top:
                if (staircase, step, staircase, step + move) in self.moves_done:
                    continue
                s += self.paths_2(staircase, step + move)
                self.moves_done.add((staircase, step, staircase, step+move))
                
                
        return s

        
        
    def part1(self):
        return self.paths(*self.stairs["S1"], self.possible_moves)
    
    def part2(self):
        self.moves_done = set() #(from_stair, from_step, to_stair, to_step)
        res = self.paths_2("S1", self.stairs["S1"][0])
        return res 
    
    def part3(self):
        return None
    
    
def main():
    start = time.perf_counter()
    
    s = Solution(test=True)
    print("---TEST---")
    print(f"part 1: {s.part1()}")
    print(f"part 2: {s.part2()}")
    print(f"part 3: {s.part3()}\n")
    
    s = Solution()
    print("---MAIN---")
    print(f"part 1: {s.part1()}")
    part2 = s.part2()
    assert part2 != 115790115638940139516655311982964
    print(f"part 2: {part2}")
    print(f"part 3: {s.part3()}")
    
    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    
main()