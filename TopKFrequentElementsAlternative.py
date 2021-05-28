#347. Top K Frequent Elements,Time -> O(n)
from collections import Counter
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        res = Counter(nums)
        revDict = defaultdict(list)
        maxm = -1
        
        for item in res:
            key = item
            count = res[item]
            revDict[count].append(key)
            if count > maxm:
                maxm = count
        while len(ans)<k:
            if maxm in revDict:
                ans = ans+revDict[maxm]
            maxm = maxm -1
        
        return ans
