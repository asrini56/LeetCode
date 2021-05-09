#Time - O(n^2)
class Solution:
    def minAreaRect(self, points: List[List[int]]) -> int:
        m = {}
        for i in range(len(points)):
            if points[i][0] in m:
                m[points[i][0]].add(points[i][1])
            else:
                m[points[i][0]] = set()
                m[points[i][0]].add(points[i][1])
        area = float("inf")
        for i in range(len(points)):
            for j in range(i+1,len(points)):
                x1 = points[i][0]
                y1 = points[i][1]
                x2 = points[j][0]
                y2 = points[j][1]
                if x1 != x2 and y1 != y2:
                    if y2 in m[x1] and y1 in m[x2]:
                        area = min(area,abs(x1-x2)*abs(y1-y2))
        if area == float("inf"):
            return 0
        return area
