#875. Koko Eating Bananas, Time - O(N * log(M)) where N is no of piles & M is range of K (left to right)
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def check(middle):
            hours = 0
            for i in range(len(piles)):
                d = piles[i] // middle
                hours+=d
                if piles[i] % middle != 0:
                    hours+=1
            return hours
        left = 1
        #right = max(piles)
        right = 1000000000
        while left < right:
            middle = (left+right) // 2
            if check(middle) <= h:
                right = middle
            else:
                left = middle + 1
        return left
