#Partition Labels, Time - O(n)
class Solution:
    def partitionLabels(self, S: str) -> List[int]:
        last = {}
        for i in range(len(S)):
            last[S[i]] = i
        left = right = 0
        ans = []
        for i in range(len(S)):
            right = max(right,last[S[i]])
            if i == right:
                ans.append(right-left+1)
                left=i+1
        return ans
