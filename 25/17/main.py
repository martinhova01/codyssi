import time
from collections import defaultdict, deque
import networkx as nx
from functools import cache
import re

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
            self.G.add_edge((_from, steps[0]), (stair, steps[0]))
            self.G.add_edge((stair, steps[1]), (to, steps[1]))

        self.possible_moves = tuple(map(int, re.findall(r"\d+", possible_moves)))
    
    @cache
    def paths(self, _from, to):
        if _from == to:
            return 1
        s = 0
        for move in self.possible_moves:
            if _from + move <= to:
                s += self.paths(_from + move, to)
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
    def num_paths(self, node):
        if node == ("S1", self.stairs["S1"][1]):
            return 1
        
        next_nodes = set()
        for layer, nodes in self.bfs_layers(node).items():
            if layer not in self.possible_moves:
                continue
            next_nodes.update(nodes)
        
        s = 0
        for next_node in next_nodes:
            s += self.num_paths(next_node)
        return s
    

    def safe_path(self, node, path, rank):
        if node == ("S1", self.stairs["S1"][1]):
            return path
        
        next_nodes = set()
        for layer, nodes in self.bfs_layers(node).items():
            if layer not in self.possible_moves:
                continue
            next_nodes.update(nodes)
            
            
        next_nodes_num_paths = []
        for next_node in next_nodes:
            num_paths = self.num_paths(next_node)
            stair, step = next_node
            next_nodes_num_paths.append(((int(stair[1:]), step), num_paths))
        
        _sorted = sorted(next_nodes_num_paths)
        i = 0
        s = 0
        for i, (_, num_paths) in enumerate(_sorted):
            if rank + s + num_paths >= self.target:
                break
            s += num_paths
                
        stair, step = _sorted[i][0]
        next_node = ("S" + str(stair), step)
        new_path = path + [next_node]
        return self.safe_path(next_node, new_path, rank + s)
    
        
    def part1(self):
        return self.paths(*self.stairs["S1"])
    
    def part2(self):
        return self.num_paths(("S1", 0))
        
    
    def part3(self):
        self.target = 73287437832782344 if self.test else 100000000000000000000000000000
        start_node = ("S1", 0)
        path = self.safe_path(start_node, [start_node], 0)
        res = ""
        for stair, step in path:
            res += "-" + stair + "_" + str(step)
        return res[1:]
    
    
def main():
    start = time.perf_counter()
    
    s = Solution(test=True)
    print("---TEST---")
    print(f"part 1: {s.part1()}")
    print(f"part 2: {s.part2()}")
    print(f"part 3: {s.part3()}\n")
    
    s = Solution()
    print("---MAIN---")
    part1 = s.part1()
    assert part1 == 87539891925831589854091029
    print(f"part 1: {part1}")
    part2 = s.part2()
    assert part2 == 117690976789375726887542201766207
    print(f"part 2: {part2}")
    part3 = s.part3()
    assert part3 == "S1_0-S1_1-S1_2-S1_3-S1_4-S1_5-S1_6-S1_7-S1_8-S1_9-S1_10-S1_11-S14_12-S14_14-S14_17-S14_18-S14_20-S14_21-S14_22-S14_24-S14_27-S17_29-S17_32-S17_33-S17_39-S17_40-S17_42-S17_44-S106_44-S106_47-S25_52-S25_54-S25_55-S25_56-S25_57-S25_58-S25_60-S25_62-S25_63-S25_64-S25_65-S61_66-S61_67-S63_72-S63_73-S63_74-S104_75-S104_77-S104_78-S26_79-S26_81-S26_84-S26_87-S76_87-S76_88-S76_89-S109_90-S109_91-S109_92-S109_94-S109_95-S1_96"
    print(f"part 3: {part3}")
    
    print(f"\nTotal time: {time.perf_counter() - start : .4f} sec")
    
main()