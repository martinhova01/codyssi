import time
from collections import deque
import numpy as np

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        self.max_val = 1073741824
        self.parse()
    
    def parse(self):
        grid, instructions, flow_control_actions = self.data.split("\n\n")
        self.grid = np.array([list(map(int, line.split(" "))) for line in grid.split("\n")], dtype=np.int64)
        self.N = len(self.grid)
        self.instructions = instructions.split("\n")
        self.flow_control_actions = flow_control_actions.split("\n")[1::2]
        self.row_first = True
    
    def shift(self, idx, amount, row=True):
        if row != self.row_first:
            self.grid = np.transpose(self.grid)
            self.row_first = not self.row_first
            
        tmp = list(self.grid[idx])
        for i in range(self.N):
            self.grid[idx][(i + amount) % self.N] = tmp[i]
                
    
    def change(self, operation, amount, idx, row=True):
        if row != self.row_first:
            self.grid = np.transpose(self.grid)
            self.row_first = not self.row_first
            
        if operation == "ADD":
            for i in range(self.N):
                self.grid[idx][i] = (self.grid[idx][i] + amount) % self.max_val
                
        elif operation == "SUB":
            for i in range(self.N):
                self.grid[idx][i] = (self.grid[idx][i] - amount) % self.max_val
        else:
            for i in range(self.N):
                self.grid[idx][i] = (self.grid[idx][i] * amount) % self.max_val
                    
    def perform_instruction(self, instruction: str):
        words = instruction.split(" ")
        if words[0] == "SHIFT":
            i = int(words[2]) - 1
            amt = int(words[4])
            self.shift(i, amt, words[1] == "ROW")
            
        else:
            op = words[0]
            amt = int(words[1])
            if len(words) == 4:
                self.change(op, amt, int(words[3]) - 1, words[2] == "ROW")
            else:
                for i in range(self.N):
                    self.change(op, amt, i)
    
    def find_largest(self):
        largest = 0
        for _ in range(2):
            for row in self.grid:
                largest = max(largest, sum(row))
            self.grid = np.transpose(self.grid)
        return largest
        
        
    def part1(self):
        for instruction in self.instructions:
            self.perform_instruction(instruction)
        
        return self.find_largest()
    
                
    def part2(self):
        self.parse()
        q = deque(self.instructions)
        for action in self.flow_control_actions:
            if action == "CYCLE":
                q.append(q.popleft())
            else:
                self.perform_instruction(q.popleft())
        
        return self.find_largest()
    
    def part3(self):
        self.parse()
        q = deque(self.instructions)
        i = 0
        while q:
            action = self.flow_control_actions[i]
            if action == "CYCLE":
                q.append(q.popleft())
            else:
                self.perform_instruction(q.popleft())
            i = (i + 1) % len(self.flow_control_actions)
        
        return self.find_largest()
    
    
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
    print(f"part 2: {s.part2()}")
    print(f"part 3: {s.part3()}")
    
    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    
main()