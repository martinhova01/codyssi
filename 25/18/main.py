import time
from collections import deque
import re

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        self.limits = (3, 3, 5) if self.test else (10, 15, 60)
        self.parse()
    
    def parse(self):
        self.rules, self.velocities = [], []
        for line in self.data.split("\n"):
            rule, vel = line.split(" | ")
            x, y, z, a, div, rem = map(int, re.findall(r"\d+", rule[6:]))
            velocity = tuple(map(int, re.findall(r"-?\d+", vel)))
            self.rules.append((x, y, z, a, div, rem))
            self.velocities.append(velocity)
        
        self.debris = self.find_debris()
        

    def find_debris(self):
        debris = []
        for x in range(self.limits[0]):
            for y in range(self.limits[1]):
                for z in range(self.limits[2]):
                    for a in range(-1, 2):
                        for i, rule in enumerate(self.rules):
                            if (x * rule[0] + y * rule[1] + z * rule[2] + a * rule[3]) % rule[4] == rule[5]:
                                debris.append(((x, y, z, a), self.velocities[i]))
        return debris
        
        
    def part1(self):
        return len(self.debris)
    
    def collision_check(self, x, y, z, a):
        if (x, y, z, a) == (0, 0, 0, 0):
            return False
        for pos, _ in self.debris:
            if pos == (x, y, z, a):
                return True
        return False
    
    def time_step(self):
        new_debris = []
        for pos, vel in self.debris:
            x = (pos[0] + vel[0]) % self.limits[0]
            y = (pos[1] + vel[1]) % self.limits[1]
            z = (pos[2] + vel[2]) % self.limits[2]
            a = pos[3] + vel[3]
            sign = -1 if a > 0 else 1
            if a not in range(-1, 2):
                a = a + (3 * sign)
            new_debris.append(((x, y, z, a), (vel)))
        
        self.debris = new_debris
                
    
    def part2(self):
        visited = set()
        q = deque([(0, 0, 0, 0, 0)]) # (x, y, z, a, time_step)
        time_step = 0
        while q:
            if time_step != q[0][4]:
                self.time_step()
            x, y, z, a, time_step = q.popleft()
            
            if (x, y, z, a, time_step) in visited:
                continue
            visited.add((x, y, z, a, time_step))
            
            if self.collision_check(x, y, z, a):
                continue
            
            if (x, y, z, a) == (self.limits[0] - 1, self.limits[1] - 1, self.limits[2] - 1, 0):
                return time_step
            
            for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                if x + dx < 0 or x + dx >= self.limits[0]:
                    continue
                if y + dy < 0 or y + dy >= self.limits[1]:
                    continue
                if z + dz < 0 or z + dz >= self.limits[2]:
                    continue
                
                q.append((x + dx, y + dy, z + dz, a, time_step + 1))
            
            q.append((x, y, z, a, time_step + 1))

            
    def collisions(self, x, y, z, a) -> int:
        if (x, y, z, a) == (0, 0, 0, 0):
            return 0
        s = 0
        for pos, _ in self.debris:
            if pos == (x, y, z, a):
                s += 1
        return s
    
    def part3(self):
        self.parse()
        visited = set()
        q = deque([(0, 0, 0, 0, 0, 0)]) # (x, y, z, a, time_step, hits)
        time_step = 0
        while q:
            if time_step != q[0][4]:
                self.time_step()
            x, y, z, a, time_step, hits = q.popleft()
            
            if (x, y, z, a, time_step, hits) in visited:
                continue
            visited.add((x, y, z, a, time_step, hits))
            
            hits += self.collisions(x, y, z, a)
            if hits > 3:
                continue
            
            if (x, y, z, a) == (self.limits[0] - 1, self.limits[1] - 1, self.limits[2] - 1, 0):
                return time_step
            
            for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                if x + dx < 0 or x + dx >= self.limits[0]:
                    continue
                if y + dy < 0 or y + dy >= self.limits[1]:
                    continue
                if z + dz < 0 or z + dz >= self.limits[2]:
                    continue
                
                q.append((x + dx, y + dy, z + dz, a, time_step + 1, hits))
            
            q.append((x, y, z, a, time_step + 1, hits))
    
    
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