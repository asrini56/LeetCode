#Time - O(n)
class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        queue = deque([start])
        visited = set()
        while queue:
            node = queue.popleft()
            visited.add(node)
            if arr[node] == 0:
                return True
            if node + arr[node] < len(arr) and node + arr[node] >= 0 and node + arr[node] not in visited:
                if arr[node + arr[node]] == 0:
                    return True
                else:
                    visited.add(node+arr[node])
                    queue.append(node+arr[node])
            if node - arr[node] < len(arr) and node - arr[node] >= 0 and node - arr[node] not in visited:
                if arr[node - arr[node]] == 0:
                    return True
                else:
                    visited.add(node-arr[node])
                    queue.append(node-arr[node])
        return False
