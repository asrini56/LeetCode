#54. Spiral Matrix
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        result = []
        sc = 0
        sr = 0
        ec = len(matrix[0])-1
        er = len(matrix)-1
        while sc <= ec and sr <= er:
            for i in range(sc,ec+1):
                result.append(matrix[sr][i])
            sr = sr + 1
            for i in range(sr,er+1):
                result.append(matrix[i][ec])
            ec = ec - 1
            if sr<=er:
                for i in range(ec,sc-1,-1):
                    result.append(matrix[er][i])
                er = er - 1
            if sc<=ec:
                for i in range(er,sr-1,-1):
                    result.append(matrix[i][sc])
                sc = sc + 1
        return result
