import time
import networkx as nx
import math
import re

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        self.G = self.create_graph()
    
    def create_graph(self):
        G = nx.DiGraph()
        for _from, to, num in re.findall(r"(\w+) -> (\w+) \| (\d+)", self.data):
            G.add_edge(_from, to, w=int(num))
        return G
        
    def part1(self):
        paths = nx.single_source_shortest_path_length(self.G, "STT")
        return math.prod(sorted(paths.values(), reverse=True)[:3])
    
    def part2(self):
        paths = nx.single_source_dijkstra_path_length(self.G, "STT", weight="w")
        return math.prod(sorted(paths.values(), reverse=True)[:3])
    
    def part3(self):
        cycles = nx.cycles.simple_cycles(self.G)
        longest = 0
        for cycle in cycles:
            cycle.append(cycle[0])
            length = sum(self.G[u][v]["w"] for u, v in zip(cycle, cycle[1:]))
            longest = max(longest, length)
        return longest
        
    
    
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