import time
import networkx as nx
import numpy as np
import copy

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = np.array([list(map(int, line.split(" "))) for line in open(self.filename).read().rstrip().split("\n")])
        self.R = len(self.data)
        self.C = len(self.data[0])
        self.G = self.create_graph()
        
    def create_graph(self):
        G = nx.DiGraph()
        for y in range(self.R):
            for x in range(self.C):
                for dx, dy in ((1, 0), (0, 1)):  
                    if x + dx >= self.C or y + dy >= self.R:
                        continue
                    G.add_edge((x, y), (x + dx, y + dy), w=self.data[y + dy][x + dx])
        G.add_edge((-1, -1), (0, 0), w=self.data[0][0])
        return G
        
    def part1(self):
        safest = float("inf")
        grid = copy.deepcopy(self.data)
        for _ in range(2):
            for row in grid:
                safest = min(safest, sum(row))
            grid = np.transpose(grid)
        return safest
    
    def part2(self):
        return nx.shortest_path_length(self.G, (-1, -1), (14, 14), weight="w")  
    
    def part3(self):
        target = (self.C - 1, self.R - 1)
        return nx.shortest_path_length(self.G, (-1, -1), target, weight="w")
    
    
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