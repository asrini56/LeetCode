#296. Best Meeting Point, Time - O(mnlogmn)
class Solution:
    def get_building_points(self, grid):
        M,N = len(grid),len(grid[0])
        rows,cols = [], []
        for i in range(M):
            for j in range(N):
                if grid[i][j] == 1:
                    rows.append(i)
                    cols.append(j)
        return rows, cols
    
    def get_median_co_ordinates(self, rows, cols):
        rows.sort()
        cols.sort()
        x_median, y_median = rows[len(rows)//2], cols[len(cols)//2]
        return x_median, y_median
    
    def minTotalDistance(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        rows, cols = self.get_building_points(grid)
        x_median, y_median = self.get_median_co_ordinates(rows, cols)
        
        result = 0
        for x in rows:
            result += abs(x_median-x)
        for y in cols:
            result += abs(y_median-y)
        return result
