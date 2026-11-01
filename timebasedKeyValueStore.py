class TimeMap:

    def __init__(self):
        self.keyStore = collections.defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.keyStore[key].append([timestamp, value])

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.keyStore:
            return ""
        arr = self.keyStore[key]
        
        def binarySearch(i:int, j:int, t:int, arr:list[list]):
            res = ""
            while i <= j:
                middle = (i+j) // 2
                if arr[middle][0] <= t:
                    res = arr[middle][1]
                    i = middle+1
                else:
                    j = middle-1
            return res
        
        return binarySearch(0,len(arr)-1, timestamp, arr)

"""
def set(self, key: str, value: str, timestamp: int) -> None:
    arr = self.keyStore[key]
    
    # Fast path: if empty or greater than the latest timestamp, append in O(1)
    if not arr or timestamp >= arr[-1][0]:
        arr.append([timestamp, value])
        return
        
    # Slow path: Out-of-order arrival, find position and insert O(N)
    low, high = 0, len(arr)
    while low < high:
        mid = (low + high) // 2
        if arr[mid][0] < timestamp:
            low = mid + 1
        else:
            high = mid
            
    arr.insert(low, [timestamp, value])
"""
        


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
