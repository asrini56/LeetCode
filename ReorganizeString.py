#767. Reorganize String
import collections
class Solution:
    def reorganizeString(self, S: str) -> str:
        if not S:
            return S
        counter = collections.Counter(S)
        lists = []
        for c in counter.keys():
            lists.append([int(-counter[c]),c])
        heapq.heapify(lists)
        maxi = -1 * lists[0][0]
        if maxi > (len(S)+1)//2:
            return ""
        result = [''] * len(S)
        i = 0
        while lists:
            count,char = heapq.heappop(lists)
            count*=-1
            for j in range(count):
                result[i] = char
                i+=2
                if i >= len(S):
                    i = 1
        return "".join(result)
