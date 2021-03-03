#706. Design HashMap, Time - O(N/K)
class MyHashMap:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.capacity = 1000
        self.hash_map = [[] for i in range(self.capacity)]
    
    def hash(self, key):
        index = key % self.capacity 
        return index

    def put(self, key: int, value: int) -> None:
        """
        value will always be non-negative.
        """
        k = self.hash(key)
        bucket = self.hash_map[k]
        found = False
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i][1] = value
                found = True
                break
        if not found:
            bucket.append([key, value])
        

    def get(self, key: int) -> int:
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        """
        k = self.hash(key)
        bucket = self.hash_map[k]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                return bucket[i][-1]
        return -1

    def remove(self, key: int) -> None:
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        """
        k = self.hash(key)
        bucket = self.hash_map[k]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                temp = bucket[i]
                bucket[i] = bucket[0]
                bucket[0] = temp
                bucket.pop(0)
                break
                


# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)
