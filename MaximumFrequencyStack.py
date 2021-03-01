#895. Maximum Frequency Stack, Time - O(1)
from collections import Counter,OrderedDict
class FreqStack:

    def __init__(self):
        self.result = {}
        self.stackFreq = {}
        self.maximum = 0
        
    def push(self, x: int) -> None:
        if x in self.result:
            self.result[x]+=1
        else:
            self.result[x] = 1
        self.maximum = max(self.maximum, self.result[x])
        if self.result[x] in self.stackFreq:
            self.stackFreq[self.result[x]].append(x)
        else:
            self.stackFreq[self.result[x]] = [x]
    def pop(self) -> int:
        res = self.stackFreq[self.maximum].pop()
        self.result[res]-=1
        if not self.stackFreq[self.maximum]:
            self.stackFreq.pop(self.maximum)
            self.maximum -= 1
        return res
        
        


# Your FreqStack object will be instantiated and called as such:
# obj = FreqStack()
# obj.push(x)
# param_2 = obj.pop()
