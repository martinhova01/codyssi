import time

import sys
sys.path.append("../..")
from utils import manhattanDist

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = list(map(eval, open(self.filename).read().rstrip().split("\n")))
        
        
    def part1(self):
        dists = sorted([manhattanDist(0, 0, x, y) for x, y in self.data])
        return dists[-1] - dists[0]
    
    def part2(self):
        islands = set(self.data)
        x1, y1 = min(islands, key=lambda pos : manhattanDist(0, 0, pos[0], pos[1]))
        islands.remove((x1, y1))
        x2, y2 = min(islands, key=lambda pos : manhattanDist(x1, y1, pos[0], pos[1]))
        return manhattanDist(x1, y1, x2, y2)
        
    
    def part3(self):
        islands = set(self.data)
        d = 0
        x, y = 0, 0
        while islands:
            nx, ny = min(islands, key=lambda pos : manhattanDist(x, y, pos[0], pos[1]))
            d += manhattanDist(x, y, nx, ny)
            x, y = nx, ny
            islands.remove((nx, ny))
        return d
            
    
    
def main():
    start = time.perf_counter()
    
    s = Solution(test=True)
    print("---TEST---")
    print(f"part 1: {s.part1()}")
    print(f"part 2: {s.part2()}\n")
    print(f"part 3: {s.part3()}\n")
    
    s = Solution()
    print("---MAIN---")
    print(f"part 1: {s.part1()}")
    print(f"part 2: {s.part2()}")
    print(f"part 3: {s.part3()}")
    
    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    
main()