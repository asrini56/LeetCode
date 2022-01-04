class Solution:
    def isToeplitzMatrix(self, matrix: List[List[int]]) -> bool:
        group = {}
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if row-col not in group:
                    group[row-col] = matrix[row][col]
                else:
                    if group[row-col] != matrix[row][col]:
                        return False
        return True
