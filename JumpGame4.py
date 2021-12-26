#1345. Jump Game IV, Time/Space - O(N)
class Solution:
    def minJumps(self, arr: List[int]) -> int:
        if len(arr) == 1:
            return 0
        Map = {}
        for i in range(len(arr)):
            if arr[i] in Map.keys():
                Map[arr[i]].append(i)
            else:
                Map[arr[i]] = [i]
        queue = collections.deque([0])
        steps = 0
        while queue:
            steps+=1
            size = len(queue)
            for i in range(size):
                j = queue.popleft()
                if j - 1 >=0 and arr[j-1] in Map:
                    queue.append(j-1)
                if j + 1 <len(arr) and arr[j+1] in Map:
                    if j+1 == len(arr)-1:
                        return steps
                    queue.append(j+1)
                if arr[j] in Map:
                    for value in Map[arr[j]]:
                        if value != j:
                            if value == len(arr)-1:
                                return steps
                            queue.append(value)
                if arr[j] in Map:
                    del Map[arr[j]]
        return steps
                    
        
