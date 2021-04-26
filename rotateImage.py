#Rotate Image, Time - O(M)
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        matrix.reverse()
        for i in range(len(matrix)):
            for j in range(len(matrix)-1,i-1,-1):
                matrix[i][j],matrix[j][i] = matrix[j][i],matrix[i][j]
        print(matrix)
       
