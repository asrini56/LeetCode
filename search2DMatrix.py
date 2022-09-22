#74. Search a 2D Matrix - Time - O(logn)
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix or target is None:
            return False
        def binarySearch(matrix):
            left = 0
            right = len(matrix)*len(matrix[0]) -1
            while left<=right:
                middle = (left + right)//2
                if matrix[middle//len(matrix[0])][middle%len(matrix[0])] == target:
                    return True
                elif matrix[middle//len(matrix[0])][middle%len(matrix[0])] > target:
                    right = middle - 1
                else:
                    left = middle + 1
            return False
        return binarySearch(matrix)
