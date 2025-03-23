import time

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.parse()
        
        
    def parse(self):
        self.freq, self.swaps, self.num = open(self.filename).read().rstrip().split("\n\n")
        self.freq = list(map(int, self.freq.split("\n")))
        
        swaps = []
        for line in self.swaps.split("\n"):
            x, y = line.split("-")
            swaps.append((int(x), int(y)))
        self.swaps = swaps
            
        self.num = int(self.num)
        
    def part1(self):
        res = list(self.freq)
        for i, j in self.swaps:
            res[i - 1], res[j - 1] = res[j - 1], res[i - 1]
        return res[self.num - 1]
        
    
    def part2(self):
        triplets = []
        for i in range(len(self.swaps)):
            triplets.append((*self.swaps[i], self.swaps[(i + 1) % len(self.swaps)][0]))
        
        res = list(self.freq)
        for i, j, k in triplets:
            res[j - 1], res[k - 1], res[i - 1] = res[i - 1], res[j - 1], res[k - 1]
        
        return res[self.num - 1]
            
    
    def part3(self):
        res = list(self.freq)
        for i, j in self.swaps:
            i, j = min(i, j), max(i, j)
            block_length = min(len(res) - j + 1, j - i)
            i -= 1
            j -= 1
            res = res[0:i] + res[j: j + block_length] + res[i + block_length : j] + res[i: i + block_length] + res[j + block_length:]
        
        return res[self.num - 1]
    
    
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