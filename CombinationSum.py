#39. Combination Sum
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
