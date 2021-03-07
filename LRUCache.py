#146. LRU Cache, Time - O(n)
from collections import OrderedDict
class LRUCache:
    def __init__(self,capacity):
        self.c = capacity
        self.dictionary = OrderedDict()
    
    def get(self,key):
        if key in self.dictionary:
            self.dictionary.move_to_end(key)
            return self.dictionary[key]
        return -1
    
    def put(self,key,value):
        if key in self.dictionary:
            self.dictionary[key] = value
            self.dictionary.move_to_end(key)
        else:
            self.dictionary[key] = value
            self.dictionary.move_to_end(key)
            if len(self.dictionary) > self.c:
                self.dictionary.popitem(last = False)
        
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
