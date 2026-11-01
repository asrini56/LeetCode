class Allocator:

    def __init__(self, n: int):
        self.array = [-1] * (n)
        self.map = {}
        self.n = n
    
    def allocate(self, size: int, mID: int) -> int:
        freeIndex = 0
        stIdx = -1
        cnt = 0
        stIdx = -1
        for i in range(len(self.array)):
            if self.array[i] != -1:
                cnt = 0
            else:
                cnt += 1
                if cnt == size:
                    stIdx = i - size + 1
                    break
        if stIdx != -1:
            for i in range(stIdx,stIdx+size):
                self.array[i] = mID
            if mID not in self.map:
                self.map[mID] = []
            self.map[mID].append([stIdx, size])
        return stIdx
        
        

    def freeMemory(self, mID: int) -> int:
        if mID in self.map:
            total = 0
            for i in range(len(self.map[mID])):
                stidx, size = self.map[mID][i][0], self.map[mID][i][1]
                for j in range(stidx, stidx + size):
                    self.array[j] = -1
                total += size
            del self.map[mID]
            return total
        return 0


# Your Allocator object will be instantiated and called as such:
# obj = Allocator(n)
# param_1 = obj.allocate(size,mID)
# param_2 = obj.freeMemory(mID)
