class Solution:
    def findPairs(self, nums: List[int], k: int) -> int:
        d = collections.defaultdict(int)
        for i in range(len(nums)):
            d[nums[i]]+=1
        count = 0
        for i in d:
            if (i - k) in d.keys() and k != 0:
                print(i)
                count+=1
            if k == 0:
                if d[i] > 1:
                    count+=1
        return count
