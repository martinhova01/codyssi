import time

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        self.nums = list(map(int, self.data.split("\n")[:-1]))
        self.signs = self.data.split("\n")[-1]
    
    def calculate(self):
        s = self.nums[0]
        for i, num in enumerate(self.nums[1:]):
            if self.signs[i] == "+":
                s += num
            else:
                s -= num
        return s
        
    def part1(self):
        return self.calculate()
    
    def part2(self):
        self.signs = self.signs[::-1]
        return self.calculate()
    
    def part3(self):
        self.nums = [int(str(self.nums[i]) + str(self.nums[i + 1])) for i in range(0, len(self.nums), 2)]
        return self.calculate()
    
    
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