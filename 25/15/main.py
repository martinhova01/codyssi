import time
from collections import defaultdict, deque

class Node():
    def __init__(self, code, id):
        self.code = code
        self.id = id
        self.left = None
        self.right = None

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        self.build_tree()
        
    def insert(self, u: Node):
        curr = self.root
        while True:
            if u.id > curr.id:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = u
                    return
            else:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = u
                    return
        
    def build_tree(self):
        artifacts, targets = self.data.split("\n\n")
        
        targets = targets.split("\n")
        self.target_ids = []
        for target in targets:
            code, id = target.split(" | ")
            self.target_ids.append(int(id))
        
        artifacts = artifacts.split("\n")
        root = artifacts[0].split(" | ")
        self.root: Node = Node(root[0], int(root[1]))
        
        for line in artifacts[1:]:
            code, id = line.split(" | ")
            u = Node(code, int(id))
            self.insert(u)
        
    def part1(self):
        layers = defaultdict(int)
        q = deque([(self.root, 1)]) # node, dept
        while q:
            u, dept = q.popleft()
            layers[dept] += u.id
            if u.left:
                q.append((u.left, dept + 1))
            if u.right:
                q.append((u.right, dept + 1))
        
        return max(layers.values()) * max(layers.keys())
    
    
    def find_path(self, id):
        q = deque([(self.root)])
        path = []
        while q:
            u = q.popleft()
            if not u:
                break
            path.append(u.code)
            if id == u.id:
                break
            elif id > u.id:
                q.append((u.right))
            else:
                q.append((u.left))
        return path
    
    def part2(self):
        return "-".join(self.find_path(500000))
    
    def part3(self):
        path1 = self.find_path(self.target_ids[0])
        path2 = self.find_path(self.target_ids[1])
        
        for code in reversed(path1):
            if code in path2:
                return code
    
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