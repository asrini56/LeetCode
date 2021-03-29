#36. Valid Sudoku, Time - O(1)[Bounds Given]
import collections
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        if not board:
            return True
        colDict = collections.defaultdict(set)
        boxDict = collections.defaultdict(set)
        for i in range(len(board)):
            s = set()
            for j in range(len(board[i])):
                if board[i][j] == '.':
                    continue
                box_index = (i // 3 ) * 3 + j // 3
                if board[i][j] in boxDict[box_index]:
                    return False
                if board[i][j] in s:
                    return False
                if board[i][j] in colDict[j] and board[i][j] != '.':
                    return False
                if board[i][j] != '.':
                    colDict[j].add(board[i][j])
                s.add(board[i][j])
                boxDict[box_index].add(board[i][j])
        return True
