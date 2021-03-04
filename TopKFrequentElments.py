#347. Top K Frequent Elements, Bucket Sort
from collections import Counter
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        bucket = [[] for i in range(len(nums)+1)]
        counter = Counter(nums)
        for num in counter:
            bucket[counter[num]].append(num)
        ans = []
        for b in bucket:
            if b:
                for n in b:
                    ans.append(n)
        return ans[::-1][:k]
