#347. Top K Frequent Elements, Bucket Sort - O(N)
from collections import Counter
class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        c = Counter(nums)
        freq = [[] for j in range(len(nums)+1)]
        res = []

        for key in c.keys():
            freq[c[key]].append(key)
        i = 0
        for j in range(len(freq)-1,-1,-1):
            for l in range(0, len(freq[j])):
                res.append(freq[j][l])
                i+=1
                if i == k:
                    return res
        return res

