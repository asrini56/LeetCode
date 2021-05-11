class LFUCache:
    import collections
    def __init__(self, capacity: int):
        self.maximum = capacity
        self.time = 0
        self.keyValue = collections.OrderedDict()
        self.freq = collections.OrderedDict()
        self.check = collections.OrderedDict()

    def get(self, key: int) -> int:
        if self.maximum == 0:
            return -1
        self.time+=1
        if key not in self.keyValue.keys():
            return -1
        else:
            if key in self.freq.keys():
                self.freq[key]+=1
            if key in self.check:
                del self.check[key]
            self.check[key] = self.time
            return self.keyValue[key]

    def put(self, key: int, value: int) -> None:
        if self.maximum != 0:
            self.time+=1
            if len(self.keyValue) < self.maximum or key in self.keyValue.keys():
                if key in self.check.keys():
                    del self.check[key]
                self.check[key] = self.time
                if key in self.freq.keys():
                    self.freq[key]+=1
                else:
                    self.freq[key] = 1
                self.keyValue[key] = value
            if len(self.keyValue) == self.maximum and key not in self.keyValue.keys():
                k = min(self.freq.values())
                res = [key for key in self.freq if self.freq[key] == k]
                if len(res) > 1:
                    m = self.check[res[0]]
                    index = res[0]
                    for i in range(len(res)):
                        if self.check[res[i]] < m:
                            index = res[i]
                            m = self.check[res[i]]
                    del self.keyValue[index]
                    del self.check[index]
                    del self.freq[index]
                else:
                    del self.keyValue[res[0]]
                    del self.check[res[0]]
                    del self.freq[res[0]]
                self.keyValue[key] = value
                self.check[key] = self.time
                self.freq[key] = 1


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
