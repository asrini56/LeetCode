#40. Combination Sum II, Time - O(2^n), Space - O(n)
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        ans = []
        def backtrack(remain,curr,st):
            if remain == 0:
                ans.append(list(curr))
                return
            elif remain < 0:
                return
            for i in range(st,len(candidates)):
                if i > st and candidates[i] == candidates[i-1]:
                    continue
                curr.append(candidates[i])
                backtrack(remain-candidates[i],curr,i+1)
                curr.pop()
        candidates.sort()
        backtrack(target,[],0)
        return ans
    """
    working:-
    c = [2,5,2,1,2], t = 5
    c = [1,2,2,2,5]
    bt(5,[],0):
        r == 0 - x
        remain < 0 - x
        i in (0,5):
            0 > 0 and c[0] == c[-1] - x
            curr = [1]
            bt(4,curr,1):
                1 > 1 and c[0] == c[1]:
                curr = [1,2]
                bt(2,[],2):
                    curr = [1,2,2]
                        bt(0,curr,3):
                            remain == 0 : ans.append([1,2,2])
            ans = [[1,2,2]]
            curr.pop(1) = curr-[]
        ... i = 4:
            curr = [5]
            bt(0,[5],i+1)
            remain == 0 : ans.append(curr)
        ans = [[1,2,2],[5]]           
    """
