class Solution:
    def shortestBridge(self, A: List[List[int]]) -> int:    
        m = len(A)
        n = len(A[0])

        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        seen = set()

        for i in range(m):
            for j in range(n):
                if A[i][j] == 1:
                    queue = collections.deque([(i,j)])
                    seen.add((i,j))
                    # traverse first island
                    while queue:
                        cur_i, cur_j = queue.popleft()

                        for d in directions:
                            new_i = cur_i + d[0]
                            new_j = cur_j + d[1]

                            if 0 <= new_i < m and 0 <= new_j < n and A[new_i][new_j] == 1 and (new_i, new_j) not in seen:
                                queue.append((new_i, new_j))
                                seen.add((new_i, new_j))

                    # expand the first island:       
                    print(seen)
                    queue = collections.deque(seen)
                    distance = 0

                    while queue:
                        for _ in range(len(queue)):
                            cur_i, cur_j = queue.popleft()

                            # distance > 0 to make sure this 1 is not the one from first island
                            if A[cur_i][cur_j] == 1 and distance > 0:
                                return distance - 1

                            for d in directions:
                                new_i = cur_i + d[0]
                                new_j = cur_j + d[1]

                                if 0 <= new_i < m and 0 <= new_j < n and (new_i, new_j) not in seen:
                                    queue.append((new_i, new_j))
                                    seen.add((new_i, new_j))

                        distance += 1
