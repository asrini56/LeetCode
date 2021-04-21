#Design Search Autocomplete System , Time - O(k*l+26), input - O(s + mlogm)
from collections import defaultdict
from queue import PriorityQueue

class AutocompleteSystem:
    
    def __init__(self, sentences: List[str], times: List[int]):
        self.values = defaultdict(int)
        self.top = defaultdict(set)
        self.query = ''
        
        for i, s in enumerate(sentences):
            val = times[i]
            self.values[s] = val
            self.addSentence(s)
            

    def addSentence(self, s):
        for j in range(len(s)):
            k = s[:j+1]
            if s in self.top[k]:
                continue
            self.top[k].add(s)
            if len(self.top[k]) > 3:
                self.delsmallest(k, self.top[k])
    
    def delsmallest(self, k, top):
        top = sorted(list(top), key = lambda x: (-self.values[x], x))
        top.pop()
        top = set(top)
        self.top[k] = top
        
    def input(self, c: str) -> List[str]:
        if c == '#':
            self.values[self.query] += 1
            self.addSentence(self.query)
            self.query = ''
            return
        
        self.query += c
        if self.query in self.top:
            return sorted(list(self.top[self.query]), key = lambda x: (-self.values[x], x))
        else:
            return []
        


# Your AutocompleteSystem object will be instantiated and called as such:
# obj = AutocompleteSystem(sentences, times)
# param_1 = obj.input(c)
