import time
import numpy as np
import re

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        functions, data = open(self.filename).read().rstrip().split("\n\n")
        self.functions = list(map(int, re.findall(r"\d+", functions)))
        self.qualities = list(map(int, re.findall(r"\d+", data)))
        
    
    def apply(self, quality):
        return quality**self.functions[2] * self.functions[1] + self.functions[0]
        
    def part1(self):
        return self.apply(int(np.median(self.qualities)))
    
    def part2(self):
        s = 0
        for quality in self.qualities:
            if quality % 2 == 0:
                s += quality
        return self.apply(s)
    
    def part3(self):
        prices = sorted([self.apply(quality) for quality in self.qualities], reverse=True)
        for price in prices:
            if price < 15000000000000:
                return int(np.round(((price - self.functions[0]) / self.functions[1]) ** (1/self.functions[2])))
    
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