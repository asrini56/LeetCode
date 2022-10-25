#1871. Jump Game VII, Time/Space - O(n)
class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        farthest = 0
        queue = deque([0])
        while queue:
            node = queue.popleft()
            start = max(farthest+1,node+minJump)
            for j in range(start,min(len(s),node+maxJump+1)):
                if s[j] == "0":
                    if j == len(s)-1:
                        return True
                    queue.append(j)
            farthest = node + maxJump
        return False
