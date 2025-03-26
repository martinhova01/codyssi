import time
import re
from collections import deque

class Solution():
    def __init__(self, test=False):
        self.test = test
        self.filename = "testinput.txt" if self.test else "input.txt"
        self.parse()
        
        
    def parse(self):
        balances, transactions = open(self.filename).read().rstrip().split("\n\n")
        self.balances = {}
        for line in balances.split("\n"):
            owner, balance = line.split(" HAS ")
            self.balances[owner] = int(balance)
            
        self.transactions = []
        for match in re.findall(r"FROM ([A-Za-z-]+) TO ([A-Za-z-]+) AMT (\d+)", transactions):
            _from, to, amt = match
            self.transactions.append((_from, to, int(amt)))
            
    def top_3_balances(self):
        return sum(list(sorted(map(lambda x : x[1], self.balances.items()), reverse=True))[:3])
        
    def part1(self):
        for _from, to, amt in self.transactions:
            self.balances[to] += amt
            self.balances[_from] -= amt
            
        return self.top_3_balances()
    
    def part2(self):
        self.parse()
        for _from, to, amt in self.transactions:
            if self.balances[_from] - amt < 0:
                amt = self.balances[_from] 
                
            self.balances[to] += amt
            self.balances[_from] -= amt
            
        return self.top_3_balances()
    
    def repay_debts(self, current):
        while self.balances[current] > 0 and self.debts[current]:
            debt_to, debt_amt = self.debts[current].popleft()
            if self.balances[current] >= debt_amt:
                self.balances[debt_to] += debt_amt
                self.balances[current] -= debt_amt
            
            else:
                self.debts[current].appendleft((debt_to, debt_amt - self.balances[current]))
                self.balances[debt_to] += self.balances[current]
                self.balances[current] = 0
            
            self.repay_debts(debt_to)
            
    def part3(self):
        self.parse()
        self.debts = {}
        for key in self.balances.keys():
            self.debts[key] = deque([])
        
        for _from, to, amt in self.transactions:
            if self.balances[_from] >= amt:
                self.balances[to] += amt
                self.balances[_from] -= amt
            else:
                self.balances[to] += self.balances[_from]
                debt_amt = amt - self.balances[_from]
                self.balances[_from] = 0
                self.debts[_from].append((to, debt_amt))
            
            self.repay_debts(to)
            
        return self.top_3_balances()
                    
    
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