#1027. Longest Arithmetic Subsequence, Time - O(n^2)
class Solution:
    def longestArithSeqLength(self, A: List[int]) -> int:
        d = {}
        for i in range(1,len(A)):
            for j in range(0,i):
                diff = A[i] - A[j]
                if (j,diff) in d:
                    d[i,diff] = d[j,diff] + 1
                else:
                    d[i,diff] = 2
        return max(d.values())
