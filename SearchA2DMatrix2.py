#240. Search a 2D Matrix II
class Solution:
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """
        i = len(matrix) - 1
        j = 0
        while i < len(matrix) and i >=0 and j < len(matrix[i]) and j >= 0:
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] > target:
                i-=1
            elif matrix[i][j] < target:
                j+=1
        return False
    """
    working:
    matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
    
    i = 4, j = 0
    while .. 
    1] 18 == 5 x
    18 > 5: i = 3
    2] 10 == 5 x: i = 2
    3] 3 < 5: j = 1
    4] 6 > 5: i = 1
    5] 5==5 -> True [1,1]
    """
