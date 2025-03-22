import time

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        
    def part1(self):
        s = 0
        for c in self.data:
            if c.isalpha():
                s += 1
        return s
    
    def get_value(self, c: str):
        if c.isalpha():
            if c.isupper():
                return ord(c) - 65 + 27
            else:  
                return ord(c) - 96
        return 0
    
    def part2(self):
        s = 0
        for c in self.data:
            s += self.get_value(c)
        return s
    
    def get_value_part_3(self, c: str, pre_val: int):
        if c.isalpha():
            return self.get_value(c)
        val = pre_val * 2 - 5
        while val < 1 or val > 52:
            if val < 1:
                val += 52
            else:
                val -= 52
        return val
    
    def part3(self):
        s = self.get_value(self.data[0])
        self.values = [s]
        for i in range(1, len(self.data)):
            val = self.get_value_part_3(self.data[i], self.values[-1])
            s += val
            self.values.append(val)
        return s
    
    
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