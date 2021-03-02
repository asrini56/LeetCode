#1424. Diagonal Traverse II, Time - O(A) A-size of matrix
class Solution:
    def findDiagonalOrder(self, nums: List[List[int]]) -> List[int]:
        result = []
        dp = {}
        for i in range(len(nums)):
            for j in range(len(nums[i])):
                s = i+j
                if s in dp:
                    dp[s].append(nums[i][j])
                else:
                    dp[s] = [nums[i][j]]
        for i in range(len(dp)):
            for j in reversed(range(len(dp[i]))):
                result.append(dp[i][j])
        return result
