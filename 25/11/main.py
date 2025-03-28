import time

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.data = open(self.filename).read().rstrip()
        self.digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^"
        self.nums = self.nums_base_10()
        
    def nums_base_10(self):
        nums = []
        for line in self.data.split("\n"):
            num, base = line.split(" ")
            base = int(base)
            s = 0
            for i, c in enumerate(reversed(num)):
                s += self.digits.index(c) * base**i
            nums.append(s)
        return nums
        
    def part1(self):
        return max(self.nums)
    
    def to_base_68(self, num: int) -> str:
        res = ""
        while num > 0:
            res = self.digits[num % 68] + res
            num //= 68
        return res
    
    def part2(self):
        return self.to_base_68(sum(self.nums))
    
    def part3(self):
        _sum = sum(self.nums)
        base = 2
        while True:
            rem = _sum // base**4
            if rem == 0:
                return base
            base += 1
    
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