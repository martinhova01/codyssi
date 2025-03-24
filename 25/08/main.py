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
    
    def part2(self):
        s = 0
        for line in self.data.split("\n"):
            modified = True
            while modified:
                modified = False
                for i in range(len(line) - 1):
                    if (
                        (line[i + 1].isalpha() or line[i + 1] == "-") and line[i].isdigit()
                        or (line[i].isalpha() or line[i] == "-") and line[i + 1].isdigit()
                    ):
                        line = line[:i] + line[i + 2:]
                        modified = True
                        break
            s += len(line)
        
        return s
    
    def part3(self):
        s = 0
        for line in self.data.split("\n"):
            modified = True
            while modified:
                modified = False
                for i in range(len(line) - 1):
                    if (
                        line[i + 1].isalpha() and line[i].isdigit()
                        or line[i].isalpha() and line[i + 1].isdigit()
                    ):
                        line = line[:i] + line[i + 2:]
                        modified = True
                        break
            s += len(line)
        
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