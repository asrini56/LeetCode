#39. Combination Sum
"""
Let N be the number of candidates, T be the target value, and M be the minimal value among the candidates.
Time - O(n^T/M +1), SPACE - O(T/M) RECURSION DEPTH
"""
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        ans = []
        def backtrack(remain,curr,st):
            if remain == 0:
                ans.append(list(curr))
                return
            elif remain < 0:
                return
            for i in range(st,len(candidates)):
                curr.append(candidates[i])
                backtrack(remain-candidates[i],curr,i)
                curr.pop()
        backtrack(target,[],0)
        return ans
